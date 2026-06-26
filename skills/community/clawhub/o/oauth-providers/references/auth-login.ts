/**
 * auth-login.ts
 *
 * Gateway RPCs for OAuth and subscription-token authentication flows.
 *
 *   auth.login.status              → list configured auth profiles
 *   auth.login.anthropic-token     → store an Anthropic setup-token
 *   auth.login.anthropic-auto      → auto-detect token from claude CLI credentials
 *   auth.login.openai-codex        → run OpenAI Codex PKCE OAuth (opens browser)
 *   auth.login.remove              → remove a profile by profileId
 */

import { readFile } from "node:fs/promises";
import { homedir } from "node:os";
import { join } from "node:path";
import type { OpenClawConfig } from "../../config/config.js";
import {
  readConfigFileSnapshot,
  writeConfigFile,
} from "../../config/io.js";
import { resolveUserPath } from "../../utils.js";
import {
  loadAuthProfileStore,
  saveAuthProfileStore,
  setAuthProfileOrder,
  upsertAuthProfile,
} from "../../agents/auth-profiles.js";
import { applyAuthProfileConfig } from "../../commands/onboard-auth.config-core.js";
import { buildTokenProfileId, validateAnthropicSetupToken } from "../../commands/auth-token.js";
import { openUrl } from "../../commands/onboard-helpers.js";
import { ErrorCodes, errorShape } from "../protocol/index.js";
import type { GatewayRequestHandlers } from "./types.js";

// ─── Helpers ──────────────────────────────────────────────────────────────────

/** Default agent directory (same convention as secrets.ts) */
function defaultAgentDir(): string {
  return resolveUserPath("~/.openclaw/agents/main/agent");
}

async function patchConfig(
  mutate: (cfg: OpenClawConfig) => OpenClawConfig,
): Promise<void> {
  const snapshot = await readConfigFileSnapshot();
  const base: OpenClawConfig = snapshot.valid ? snapshot.config : {};
  const next = mutate(base);
  await writeConfigFile(next);
}

// ─── Status ───────────────────────────────────────────────────────────────────

async function getAuthStatus(): Promise<{
  ok: boolean;
  profiles: Array<{ profileId: string; provider: string; mode: string; email?: string }>;
}> {
  const snapshot = await readConfigFileSnapshot();
  const cfg: OpenClawConfig = snapshot.valid ? snapshot.config : {};
  const profiles: Array<{ profileId: string; provider: string; mode: string; email?: string }> = [];
  for (const [profileId, profile] of Object.entries(cfg.auth?.profiles ?? {})) {
    const p = profile as { provider: string; mode: string; email?: string };
    profiles.push({ profileId, provider: p.provider, mode: p.mode, email: p.email });
  }
  return { ok: true, profiles };
}

// ─── Anthropic setup-token ────────────────────────────────────────────────────

async function storeAnthropicSetupToken(
  token: string,
  profileName?: string,
): Promise<{ ok: boolean; profileId?: string; error?: string }> {
  const trimmed = token.trim();
  const validationError = validateAnthropicSetupToken(trimmed);
  if (validationError) {
    return { ok: false, error: `Invalid setup token: ${validationError}` };
  }

  const agentDir = defaultAgentDir();
  const provider = "anthropic";
  const profileId = buildTokenProfileId({ provider, name: profileName ?? "default" });

  upsertAuthProfile({
    profileId,
    agentDir,
    credential: { type: "token", provider, token: trimmed },
  });

  await patchConfig((cfg) =>
    applyAuthProfileConfig(cfg, { profileId, provider, mode: "token" }),
  );

  // Ensure the new profile is listed first in the store order so it takes
  // priority over any existing API key profiles (store order wins over openclaw.json).
  const currentStore = loadAuthProfileStore(agentDir);
  const existingOrder: string[] = Array.isArray(currentStore.order?.[provider])
    ? (currentStore.order![provider] as string[])
    : Object.keys(currentStore.profiles ?? {}).filter(
        (id) => currentStore.profiles[id]?.provider === provider,
      );
  const newOrder = [profileId, ...existingOrder.filter((id) => id !== profileId)];
  await setAuthProfileOrder({ agentDir, provider, order: newOrder });

  return { ok: true, profileId };
}

// ─── Anthropic auto-detect (from claude CLI) ─────────────────────────────────

/**
 * Read the token from the claude CLI credentials file (~/.claude/.credentials.json)
 * and store it directly as an Anthropic subscription token profile.
 * 
 * Claude CLI stores an sk-ant-oat01-... OAuth access token that OpenClaw can use directly.
 */
async function autoDetectAnthropicToken(profileName?: string): Promise<{
  ok: boolean;
  profileId?: string;
  error?: string;
  token?: string;
}> {
  const credPath = join(homedir(), ".claude", ".credentials.json");
  let raw: string;
  try {
    raw = await readFile(credPath, "utf-8");
  } catch {
    return {
      ok: false,
      error: `Claude CLI credentials not found at ${credPath}. Make sure claude is installed and you have signed in with 'claude'.`,
    };
  }

  let creds: unknown;
  try {
    creds = JSON.parse(raw);
  } catch {
    return { ok: false, error: "Failed to parse claude CLI credentials file." };
  }

  const oauthData = (creds as Record<string, unknown>)?.claudeAiOauth as Record<string, unknown> | undefined;
  if (!oauthData) {
    return {
      ok: false,
      error: "No claudeAiOauth credentials found in claude CLI credentials. Sign in with 'claude' first.",
    };
  }

  const accessToken = typeof oauthData.accessToken === "string" ? oauthData.accessToken.trim() : "";
  const expiresAt = typeof oauthData.expiresAt === "number" ? oauthData.expiresAt : 0;

  if (!accessToken) {
    return { ok: false, error: "No accessToken found in claude CLI credentials." };
  }

  const validationError = validateAnthropicSetupToken(accessToken);
  if (validationError) {
    return {
      ok: false,
      error: `Claude CLI token format unexpected: ${validationError}. Token starts with: ${accessToken.slice(0, 15)}...`,
    };
  }

  // Warn if token is expired but still try to use it (Anthropic may still accept it or user can re-auth)
  const now = Date.now();
  if (expiresAt > 0 && expiresAt < now) {
    console.warn("[auth-login] Claude CLI OAuth token appears expired. Attempting to use anyway.");
  }

  const result = await storeAnthropicSetupToken(accessToken, profileName ?? "claude-cli");
  if (!result.ok) {
    return result;
  }
  return { ok: true, profileId: result.profileId, token: accessToken };
}

// ─── OpenAI Codex OAuth ───────────────────────────────────────────────────────

/** In-progress OAuth sessions: sessionId → { url, resultPromise, submitCode? } */
type PendingOAuthSession = {
  url: string;
  resultPromise: Promise<{ ok: boolean; profileId?: string; email?: string; error?: string }>;
  /** Resolve this with the pasted redirect URL / code to complete the flow manually */
  submitCode?: (input: string) => void;
};
const pendingOAuthSessions = new Map<string, PendingOAuthSession>();

/**
 * Start the OAuth flow. Returns the auth URL immediately so the UI can display
 * a clickable link. The underlying flow continues in the background.
 * Call `pollOpenAICodexOAuth(sessionId)` to await the final result.
 */
async function startOpenAICodexOAuth(): Promise<{
  ok: boolean;
  sessionId?: string;
  url?: string;
  error?: string;
}> {
  const agentDir = defaultAgentDir();

  type PiAi = typeof import("@mariozechner/pi-ai");
  let piAi: PiAi;
  try {
    piAi = await import("@mariozechner/pi-ai");
  } catch {
    return { ok: false, error: "@mariozechner/pi-ai is not installed." };
  }

  const { loginOpenAICodex } = piAi;

  // Deferred for when the auth URL becomes available
  let resolveUrl!: (url: string) => void;
  let rejectUrl!: (err: unknown) => void;
  const urlReady = new Promise<string>((res, rej) => {
    resolveUrl = res;
    rejectUrl = rej;
  });

  // Deferred for manual code/URL submission (fallback when localhost callback fails)
  let resolveManualCode!: (input: string) => void;
  let rejectManualCode!: (err: unknown) => void;
  const manualCodePromise = new Promise<string>((res, rej) => {
    resolveManualCode = res;
    rejectManualCode = rej;
  });

  // Run the full OAuth flow in the background
  const resultPromise: Promise<{ ok: boolean; profileId?: string; email?: string; error?: string }> =
    (async () => {
      let creds: Awaited<ReturnType<typeof loginOpenAICodex>> | null = null;
      try {
        creds = await loginOpenAICodex({
          onAuth: (info) => {
            // Surface the URL to the UI instead of trying to open a popup
            resolveUrl(info.url);
          },
          // Race between the local callback server and the user pasting the redirect URL
          onManualCodeInput: () => manualCodePromise,
          onPrompt: async () => "",
          onProgress: (msg) => {
            console.log("[auth-login] OAuth progress:", msg);
          },
        });
      } catch (err) {
        // If onAuth was never called, reject the URL promise too
        rejectUrl(err);
        // Also reject the manual code promise to avoid memory leaks
        rejectManualCode(err);
        return { ok: false, error: `OAuth flow failed: ${String(err)}` };
      }

      if (!creds) {
        return { ok: false, error: "OAuth cancelled or no credentials returned." };
      }

      const { writeOAuthCredentials } = await import("../../commands/onboard-auth.credentials.js");
      const { applyOpenAICodexModelDefault } = await import(
        "../../commands/openai-codex-model-default.js"
      );

      const profileId = await writeOAuthCredentials("openai-codex", creds, agentDir, {
        syncSiblingAgents: true,
      });

      await patchConfig((cfg) => {
        let next = applyAuthProfileConfig(cfg, {
          profileId,
          provider: "openai-codex",
          mode: "oauth",
        });
        const applied = applyOpenAICodexModelDefault(next);
        if (applied.changed) next = applied.next;
        return next;
      });

      const credsRecord = creds as Record<string, unknown>;
      const email = typeof credsRecord["email"] === "string" ? credsRecord["email"] : undefined;
      return { ok: true, profileId, email };
    })();

  // Wait until the auth URL is ready (or the flow errors before producing one)
  let url: string;
  try {
    url = await urlReady;
  } catch (err) {
    return { ok: false, error: `Failed to start OAuth: ${String(err)}` };
  }

  const sessionId = `oauth-${Date.now()}-${Math.random().toString(36).slice(2, 8)}`;
  pendingOAuthSessions.set(sessionId, { url, resultPromise, submitCode: resolveManualCode });

  return { ok: true, sessionId, url };
}

/**
 * Wait for an in-progress OAuth session (started via startOpenAICodexOAuth) to complete.
 */
async function pollOpenAICodexOAuth(sessionId: string): Promise<{
  ok: boolean;
  profileId?: string;
  email?: string;
  error?: string;
}> {
  const session = pendingOAuthSessions.get(sessionId);
  if (!session) {
    return { ok: false, error: "No active OAuth session. Please start the flow again." };
  }
  try {
    const result = await session.resultPromise;
    pendingOAuthSessions.delete(sessionId);
    return result;
  } catch (err) {
    pendingOAuthSessions.delete(sessionId);
    return { ok: false, error: String(err) };
  }
}

// ─── Remove profile ───────────────────────────────────────────────────────────

async function removeProfile(profileId: string): Promise<{ ok: boolean; error?: string }> {
  const agentDir = defaultAgentDir();

  // Remove from auth-profiles.json
  const store = loadAuthProfileStore();
  const profiles = { ...(store.profiles ?? {}) };
  delete profiles[profileId];
  saveAuthProfileStore({ ...store, profiles }, agentDir);

  // Remove from openclaw.json
  await patchConfig((cfg) => {
    const cfgProfiles = { ...(cfg.auth?.profiles ?? {}) };
    delete cfgProfiles[profileId];
    const order: Record<string, string[]> = {};
    for (const [provider, ids] of Object.entries(cfg.auth?.order ?? {})) {
      order[provider] = (ids as string[]).filter((id) => id !== profileId);
    }
    return { ...cfg, auth: { ...cfg.auth, profiles: cfgProfiles, order } };
  });

  return { ok: true };
}

// ─── Handlers ─────────────────────────────────────────────────────────────────

export const authLoginHandlers: GatewayRequestHandlers = {
  "auth.login.status": async ({ respond }) => {
    try {
      const result = await getAuthStatus();
      respond(true, result, undefined);
    } catch (err) {
      respond(false, undefined, errorShape(ErrorCodes.UNAVAILABLE, String(err)));
    }
  },

  "auth.login.anthropic-token": async ({ params: p, respond }) => {
    const token = (p as { token?: string })?.token?.trim();
    const profileName = (p as { profileName?: string })?.profileName;
    if (!token) {
      respond(false, undefined, errorShape(ErrorCodes.INVALID_REQUEST, "token required"));
      return;
    }
    try {
      const result = await storeAnthropicSetupToken(token, profileName);
      respond(result.ok, result, result.ok ? undefined : errorShape(ErrorCodes.INVALID_REQUEST, result.error ?? "error"));
    } catch (err) {
      respond(false, undefined, errorShape(ErrorCodes.UNAVAILABLE, String(err)));
    }
  },

  "auth.login.anthropic-auto": async ({ params: p, respond }) => {
    const profileName = (p as { profileName?: string })?.profileName;
    try {
      const result = await autoDetectAnthropicToken(profileName);
      respond(result.ok, result, result.ok ? undefined : errorShape(ErrorCodes.UNAVAILABLE, result.error ?? "error"));
    } catch (err) {
      respond(false, undefined, errorShape(ErrorCodes.UNAVAILABLE, String(err)));
    }
  },

  "auth.login.openai-codex": async ({ respond }) => {
    // Start the OAuth flow and return the URL for display in the UI.
    // The client should then call auth.login.openai-codex.poll with the returned sessionId.
    try {
      const result = await startOpenAICodexOAuth();
      respond(
        result.ok,
        result,
        result.ok ? undefined : errorShape(ErrorCodes.UNAVAILABLE, result.error ?? "error"),
      );
    } catch (err) {
      respond(false, undefined, errorShape(ErrorCodes.UNAVAILABLE, String(err)));
    }
  },

  "auth.login.openai-codex.poll": async ({ params: p, respond }) => {
    const sessionId = (p as { sessionId?: string })?.sessionId?.trim();
    if (!sessionId) {
      respond(false, undefined, errorShape(ErrorCodes.INVALID_REQUEST, "sessionId required"));
      return;
    }
    try {
      const result = await pollOpenAICodexOAuth(sessionId);
      respond(
        result.ok,
        result,
        result.ok ? undefined : errorShape(ErrorCodes.UNAVAILABLE, result.error ?? "error"),
      );
    } catch (err) {
      respond(false, undefined, errorShape(ErrorCodes.UNAVAILABLE, String(err)));
    }
  },

  "auth.login.openai-codex.submit-code": async ({ params: p, respond }) => {
    // Submit a manually-pasted redirect URL or code to complete the OAuth flow.
    // Used as a fallback when the localhost callback server is unreachable (e.g., WSL2).
    const sessionId = (p as { sessionId?: string })?.sessionId?.trim();
    const input = (p as { input?: string })?.input?.trim();
    if (!sessionId) {
      respond(false, undefined, errorShape(ErrorCodes.INVALID_REQUEST, "sessionId required"));
      return;
    }
    if (!input) {
      respond(false, undefined, errorShape(ErrorCodes.INVALID_REQUEST, "input required"));
      return;
    }
    const session = pendingOAuthSessions.get(sessionId);
    if (!session) {
      respond(false, undefined, errorShape(ErrorCodes.INVALID_REQUEST, "No active OAuth session for this sessionId."));
      return;
    }
    if (!session.submitCode) {
      respond(false, undefined, errorShape(ErrorCodes.UNAVAILABLE, "Manual code submission not supported for this session."));
      return;
    }
    session.submitCode(input);
    respond(true, { ok: true }, undefined);
  },

  "auth.login.remove": async ({ params: p, respond }) => {
    const profileId = (p as { profileId?: string })?.profileId?.trim();
    if (!profileId) {
      respond(false, undefined, errorShape(ErrorCodes.INVALID_REQUEST, "profileId required"));
      return;
    }
    try {
      const result = await removeProfile(profileId);
      respond(result.ok, result, result.ok ? undefined : errorShape(ErrorCodes.UNAVAILABLE, result.error ?? "error"));
    } catch (err) {
      respond(false, undefined, errorShape(ErrorCodes.UNAVAILABLE, String(err)));
    }
  },
};
