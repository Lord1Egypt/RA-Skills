import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import { AMBIENT_SSO_TIER } from "./config.js";

const CRED_DIR = path.join(os.homedir(), ".hawkeye-lead-cli");
const CRED_FILE = path.join(CRED_DIR, "credentials.json");

// 公司里跑在 codewiz/seal/OpenClaw 这类 agent 环境中时，这个文件通常已经自带登录态
// （由 SSO 体系统一维护，多个内部 CLI 共用这个约定）。手动设置的 token 优先级更高，
// 这个文件只在没有手动设置时兜底用。
//
// 根因已跟 merchant_lead 接口负责人确认：这批接口在 edith 网关层挂了专门的 SSO 插件，
// 这个插件目前认的是"专门针对被访问域名签发的 cookie"，不认这里读到的 ambient token
// （见 apiClient.js 顶部注释）。跟"服务是否稳定"没关系，纯粹是这个插件的校验方式决定的；
// 上线到正式域名后这个插件会不会认 ambient token 尚未实测确认，不要假设一定会免登录。
const AMBIENT_SSO_FILE = path.join(os.homedir(), ".token", "sso_token.json");

function readAmbientSsoToken() {
  if (!fs.existsSync(AMBIENT_SSO_FILE)) return null;
  try {
    const data = JSON.parse(fs.readFileSync(AMBIENT_SSO_FILE, "utf8"));
    return data[`common-internal-access-token-${AMBIENT_SSO_TIER}`] || null;
  } catch {
    return null;
  }
}

function readCredentials() {
  if (!fs.existsSync(CRED_FILE)) return null;
  try {
    return JSON.parse(fs.readFileSync(CRED_FILE, "utf8"));
  } catch {
    return null;
  }
}

function writeCredentials(data) {
  fs.mkdirSync(CRED_DIR, { recursive: true, mode: 0o700 });
  fs.writeFileSync(CRED_FILE, JSON.stringify(data, null, 2));
  fs.chmodSync(CRED_FILE, 0o600);
}

export function setToken(token) {
  if (!token || !token.trim()) {
    throw new Error("token 不能为空");
  }
  writeCredentials({ token: token.trim(), capturedAt: new Date().toISOString() });
}

export function getToken() {
  const creds = readCredentials();
  if (creds?.token) return creds.token;
  return readAmbientSsoToken();
}

export function maskToken(token) {
  if (!token) return "(未设置)";
  return token.length <= 18 ? token : `${token.slice(0, 18)}…`;
}

export function getStatus() {
  const creds = readCredentials();
  if (creds?.token) {
    return {
      present: true,
      source: "manual",
      maskedToken: maskToken(creds.token),
      capturedAt: creds.capturedAt,
    };
  }
  const ambientToken = readAmbientSsoToken();
  if (ambientToken) {
    return {
      present: true,
      source: "ambient",
      maskedToken: maskToken(ambientToken),
      capturedAt: null,
    };
  }
  return { present: false };
}

export function buildCookieHeader(cookieName) {
  const token = getToken();
  if (!token) return null;
  return `${cookieName}=${token}`;
}

export const CREDENTIALS_PATH = CRED_FILE;
