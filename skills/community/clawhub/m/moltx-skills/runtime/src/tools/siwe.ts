import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import crypto from "node:crypto";

import { API_URL, API_KEY, getPrivateKey, getWalletAddress } from "./config.js";
import { getPublicRuntime, stringifyJson, toRecord, type ToolHandler } from "./shared.js";
import { privateKeyToAccount } from "viem/accounts";

// ── Auth state persistence ────────────────────────────────────────────────────

const AUTH_PATH = path.join(os.homedir(), ".moltx", "auth.json");

type AuthState = {
  accessToken: string;
  refreshToken: string;
  walletAddress: string;
  expiresAt: string; // ISO string
};

export function readStoredAuth(): AuthState | undefined {
  if (!fs.existsSync(AUTH_PATH)) return undefined;
  try {
    const raw = JSON.parse(fs.readFileSync(AUTH_PATH, "utf8"));
    if (typeof raw.accessToken !== "string" || !raw.walletAddress || !raw.expiresAt) {
      return undefined;
    }
    return raw as AuthState;
  } catch {
    return undefined;
  }
}

function writeStoredAuth(state: AuthState): void {
  const dir = path.dirname(AUTH_PATH);
  fs.mkdirSync(dir, { recursive: true, mode: 0o700 });
  fs.writeFileSync(AUTH_PATH, JSON.stringify(state, null, 2), { mode: 0o600 });
  // Enforce permissions on pre-existing files (writeFileSync mode only applies on create).
  fs.chmodSync(AUTH_PATH, 0o600);
}

/**
 * Returns the stored access token if it exists and has more than 60 seconds remaining.
 * Returns undefined if missing or expired — agent should call siwe_login or siwe_refresh.
 */
export function getStoredJwt(): string | undefined {
  const state = readStoredAuth();
  if (!state) return undefined;
  if (new Date(state.expiresAt).getTime() - Date.now() < 60_000) return undefined;
  return state.accessToken;
}

// ── SIWE message builder (EIP-4361) ──────────────────────────────────────────

function buildSiweMessage(p: {
  domain: string;
  address: string;
  statement: string;
  uri: string;
  chainId: number;
  nonce: string;
  issuedAt: string;
}): string {
  return [
    `${p.domain} wants you to sign in with your Ethereum account:`,
    p.address,
    "",
    p.statement,
    "",
    `URI: ${p.uri}`,
    `Version: 1`,
    `Chain ID: ${p.chainId}`,
    `Nonce: ${p.nonce}`,
    `Issued At: ${p.issuedAt}`,
  ].join("\n");
}

function randomNonce(): string {
  return crypto.randomBytes(16).toString("hex");
}

function requireApiBaseUrl(): string {
  return API_URL.replace(/\/+$/, "");
}

function requireApiKey(): string {
  return API_KEY;
}

// ── Tools ─────────────────────────────────────────────────────────────────────

/**
 * siwe_login — 用当前运行钱包完成 SIWE 登录。
 *
 * 原理：
 *   1. 本地构造 EIP-4361 消息并用当前运行钱包签名
 *   2. 调用 Supabase Auth 原生 Web3 接口 /auth/v1/token?grant_type=web3
 *   3. Supabase 验证签名、创建/复用用户、签发标准 Supabase session
 *   4. access_token + refresh_token 存入 ~/.moltx/auth.json
 *
 * 注意：RLS 身份校验通过 public.current_wallet() 完成，该函数有两条路径：
 *   快路径：JWT 顶层有 wallet_address claim（需注册 custom_access_token_hook）
 *   慢路径：fallback 到 auth.identities 查询（无 hook 时自动使用）
 *   两条路径均可正常工作，hook 仅为性能优化。
 *
 * 可选参数:
 *   statement: 签名说明（默认 "Sign in to MoltX"）
 */
const siwe_login: ToolHandler = async (args) => {
  const record = toRecord(args ?? {});
  const baseUrl = requireApiBaseUrl();
  const apiKey = requireApiKey();
  const { publicClient } = getPublicRuntime();
  const chainId = await publicClient.getChainId();

  const domain = new URL(baseUrl).hostname;
  const uri = baseUrl;

  const statement =
    typeof record.statement === "string" && record.statement.trim()
      ? record.statement.trim()
      : "Sign in to MoltX";

  const nonce = randomNonce();
  const issuedAt = new Date().toISOString();

  const address = await getWalletAddress();
  const message = buildSiweMessage({
    domain,
    address,
    statement,
    uri,
    chainId,
    nonce,
    issuedAt,
  });
  const account = privateKeyToAccount(getPrivateKey());
  const signature = await account.signMessage({ message });

  // Call Supabase Auth native Web3 endpoint — no custom Edge Function needed
  const res = await fetch(`${baseUrl}/auth/v1/token?grant_type=web3`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "apikey": apiKey,
    },
    body: JSON.stringify({ message, signature, chain: "ethereum" }),
  });

  if (!res.ok) {
    const body = await res.text();
    throw new Error(`SIWE login failed (${res.status}): ${body}`);
  }

  const body = await res.json();
  const accessToken: string = body.access_token;
  const refreshToken: string = body.refresh_token ?? "";
  const expiresIn: number = body.expires_in ?? 3600;

  if (!accessToken) throw new Error("No access_token returned from Supabase Auth");

  const expiresAt = new Date(Date.now() + expiresIn * 1000).toISOString();
  writeStoredAuth({ accessToken, refreshToken, walletAddress: address, expiresAt });

  return stringifyJson({
    tool: "siwe_login",
    walletAddress: address,
    domain,
    uri,
    expiresAt,
    hint: "Session stored in ~/.moltx/auth.json; API calls will use it automatically",
  });
};

/**
 * siwe_refresh — 用 refresh_token 静默续签，无需重新签名。
 * 适合 JWT 即将过期但不想重新走完整 SIWE 流程的场景。
 */
const siwe_refresh: ToolHandler = async () => {
  const state = readStoredAuth();
  if (!state?.refreshToken) {
    throw new Error("No refresh token found. Run siwe_login first.");
  }

  const baseUrl = requireApiBaseUrl();
  const apiKey = requireApiKey();

  const res = await fetch(`${baseUrl}/auth/v1/token?grant_type=refresh_token`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "apikey": apiKey,
    },
    body: JSON.stringify({ refresh_token: state.refreshToken }),
  });

  if (!res.ok) {
    const body = await res.text();
    throw new Error(`Token refresh failed (${res.status}): ${body}`);
  }

  const body = await res.json();
  const expiresIn: number = body.expires_in ?? 3600;
  const expiresAt = new Date(Date.now() + expiresIn * 1000).toISOString();

  writeStoredAuth({
    accessToken: body.access_token,
    refreshToken: body.refresh_token ?? state.refreshToken,
    walletAddress: state.walletAddress,
    expiresAt,
  });

  return stringifyJson({
    tool: "siwe_refresh",
    walletAddress: state.walletAddress,
    expiresAt,
  });
};

/**
 * siwe_logout — 清除本地存储的 session。
 */
const siwe_logout: ToolHandler = async () => {
  if (fs.existsSync(AUTH_PATH)) {
    fs.unlinkSync(AUTH_PATH);
    return stringifyJson({ tool: "siwe_logout", cleared: true });
  }
  return stringifyJson({ tool: "siwe_logout", cleared: false, hint: "No stored session found" });
};

/**
 * siwe_status — 查看当前登录状态。
 */
const siwe_status: ToolHandler = async () => {
  const envJwt = process.env.MOLTX_API_JWT?.trim();
  if (envJwt) {
    return stringifyJson({
      loggedIn: true,
      source: "MOLTX_API_JWT env var",
      hint: "JWT provided via environment variable; siwe_login is not needed",
    });
  }

  const state = readStoredAuth();
  if (!state) {
    return stringifyJson({
      loggedIn: false,
      source: null,
      hint: "Run siwe_login to authenticate",
    });
  }

  const msRemaining = new Date(state.expiresAt).getTime() - Date.now();
  const expired = msRemaining <= 0;
  const expiresInHours = Math.round(msRemaining / 3_600_000);

  return stringifyJson({
    loggedIn: !expired,
    source: AUTH_PATH,
    walletAddress: state.walletAddress,
    expiresAt: state.expiresAt,
    expiresInHours: expired ? 0 : expiresInHours,
    expired,
    hasRefreshToken: !!state.refreshToken,
    hint: expired
      ? "JWT expired — run siwe_refresh (if refresh token exists) or siwe_login"
      : expiresInHours < 24
        ? "JWT expiring soon — consider running siwe_refresh"
        : undefined,
  });
};

export const siweTools: Record<string, ToolHandler> = {
  siwe_login,
  siwe_refresh,
  siwe_logout,
  siwe_status,
};
