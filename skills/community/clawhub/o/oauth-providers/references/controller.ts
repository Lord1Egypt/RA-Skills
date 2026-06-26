import type { GatewayBrowserClient } from "../gateway.js";
import type {
  AiProvider,
  AiProviderConnectMode,
  ConnectedProfile,
} from "../views/ai-providers.js";

// ─── State Shape ─────────────────────────────────────────────────────────────

export type AiProvidersState = {
  client: GatewayBrowserClient | null;
  connected: boolean;

  aiProviders?: AiProvider[];
  aiProvidersLoading?: boolean;
  aiProvidersActiveConnect?: string | null;
  aiProvidersSelectedMode?: Record<string, AiProviderConnectMode>;
  aiProvidersPasteValues?: Record<string, string>;
  aiProvidersConnecting?: string | null;
  /** The OAuth URL to display in the card (so the user can click it without a popup) */
  aiProvidersOauthUrl?: string | null;
  /** The gateway session ID for polling OAuth completion */
  aiProvidersOauthSessionId?: string | null;
  /** Value of the "paste redirect URL" field shown during OAuth (fallback for WSL/remote) */
  aiProvidersOauthRedirectPaste?: string;
  aiProvidersMessage?: { kind: "success" | "error"; text: string } | null;
  aiProvidersRestartNeeded?: boolean;
};

// ─── Provider Catalogue ───────────────────────────────────────────────────────

const PROVIDER_CATALOGUE: Omit<AiProvider, "status" | "profiles">[] = [
  {
    id: "anthropic",
    name: "Anthropic (Claude)",
    logo: "🧠",
    color: "#d97706",
    description: "Claude Sonnet, Opus, Haiku — via API key or Claude Pro/Max subscription",
    connectOptions: [
      {
        mode: "token",
        label: "Subscription",
        hint: "Use your Claude Pro or Max subscription. Run `claude setup-token` in a terminal to get a token.",
        profileMode: "token",
      },
      {
        mode: "api-key",
        label: "API Key",
        hint: "Use an Anthropic API key from console.anthropic.com — pay-per-token, recommended for production.",
        profileMode: "api_key",
      },
    ],
  },
  {
    id: "openai",
    name: "OpenAI",
    logo: "🤖",
    color: "#10b981",
    description: "GPT-4o, o1, Codex — via ChatGPT subscription OAuth or API key",
    connectOptions: [
      {
        mode: "oauth",
        label: "ChatGPT Login",
        hint: "Sign in with your ChatGPT account (Pro/Plus). OpenAI Codex OAuth — explicitly supported for external tools.",
        profileMode: "oauth",
      },
      {
        mode: "api-key",
        label: "API Key",
        hint: "Use an OpenAI API key from platform.openai.com — pay-per-token.",
        profileMode: "api_key",
      },
    ],
  },
  {
    id: "google",
    name: "Google (Gemini)",
    logo: "✨",
    color: "#4285f4",
    description: "Gemini 2.0 Flash, Gemini 1.5 Pro, and Google AI models",
    connectOptions: [
      {
        mode: "api-key",
        label: "API Key",
        hint: "Get a free key from aistudio.google.com — generous free tier.",
        profileMode: "api_key",
      },
    ],
  },
  {
    id: "openrouter",
    name: "OpenRouter",
    logo: "🔀",
    color: "#8b5cf6",
    description: "Access 200+ models from one API — Llama, Mistral, Perplexity, and more",
    connectOptions: [
      {
        mode: "api-key",
        label: "API Key",
        hint: "Get a key from openrouter.ai — routes to dozens of model providers.",
        profileMode: "api_key",
      },
    ],
  },
];

// ─── Auth profile helpers ─────────────────────────────────────────────────────

type AuthProfileResult = {
  ok: boolean;
  profiles: Array<{
    profileId: string;
    provider: string;
    mode: "api_key" | "oauth" | "token";
    email?: string;
  }>;
};

function profilesForProvider(
  allProfiles: AuthProfileResult["profiles"],
  providerId: string,
): ConnectedProfile[] {
  return allProfiles
    .filter((p) => {
      // Match provider names including aliases
      if (providerId === "openai") return p.provider === "openai" || p.provider === "openai-codex";
      if (providerId === "anthropic") return p.provider === "anthropic";
      if (providerId === "google") return p.provider === "google" || p.provider === "gemini";
      if (providerId === "openrouter") return p.provider === "openrouter";
      return p.provider === providerId;
    })
    .map((p) => ({ profileId: p.profileId, mode: p.mode, email: p.email }));
}

// ─── Load ─────────────────────────────────────────────────────────────────────

export async function loadAiProviders(host: AiProvidersState): Promise<void> {
  if (!host.client) return;
  host.aiProvidersLoading = true;

  try {
    const result = await host.client.request<AuthProfileResult>("auth.login.status", {});

    const allProfiles = result?.profiles ?? [];

    host.aiProviders = PROVIDER_CATALOGUE.map((p): AiProvider => {
      const profiles = profilesForProvider(allProfiles, p.id);
      return {
        ...p,
        status: profiles.length > 0 ? "connected" : "not-connected",
        profiles,
      };
    });
  } catch (err) {
    console.error("[ai-providers] load failed:", err);
    host.aiProviders = PROVIDER_CATALOGUE.map((p): AiProvider => ({
      ...p,
      status: "not-connected",
      profiles: [],
    }));
  } finally {
    host.aiProvidersLoading = false;
  }
}

// ─── UI Actions ───────────────────────────────────────────────────────────────

export function aiProvidersStartConnect(host: AiProvidersState, id: string): void {
  host.aiProvidersActiveConnect = id;
  host.aiProvidersMessage = null;
}

export function aiProvidersCancel(host: AiProvidersState, id: string): void {
  if (host.aiProvidersActiveConnect === id) host.aiProvidersActiveConnect = null;
  if (host.aiProvidersConnecting === id) {
    host.aiProvidersConnecting = null;
    host.aiProvidersOauthUrl = null;
    host.aiProvidersOauthSessionId = null;
  }
  host.aiProvidersPasteValues = { ...(host.aiProvidersPasteValues ?? {}), [id]: "" };
}

export function aiProvidersSelectMode(
  host: AiProvidersState,
  id: string,
  mode: AiProviderConnectMode,
): void {
  host.aiProvidersSelectedMode = { ...(host.aiProvidersSelectedMode ?? {}), [id]: mode };
  host.aiProvidersPasteValues = { ...(host.aiProvidersPasteValues ?? {}), [id]: "" };
}

export function aiProvidersPasteChange(host: AiProvidersState, id: string, value: string): void {
  host.aiProvidersPasteValues = { ...(host.aiProvidersPasteValues ?? {}), [id]: value };
}

// ─── Save (token or api-key) ──────────────────────────────────────────────────

export async function aiProvidersSave(host: AiProvidersState, id: string): Promise<void> {
  if (!host.client) return;
  const provider = (host.aiProviders ?? []).find((p) => p.id === id);
  if (!provider) return;

  const value = (host.aiProvidersPasteValues ?? {})[id]?.trim();
  if (!value) return;

  const mode = (host.aiProvidersSelectedMode ?? {})[id] ?? provider.connectOptions[0]?.mode;

  try {
    if (id === "anthropic" && mode === "token") {
      // Anthropic setup-token
      const result = await host.client.request<{ ok: boolean; profileId?: string; error?: string }>(
        "auth.login.anthropic-token",
        { token: value },
      );
      if (result?.ok) {
        host.aiProvidersMessage = { kind: "success", text: "✅ Anthropic subscription token saved! Connected via Claude Pro/Max." };
        host.aiProvidersActiveConnect = null;
        host.aiProvidersPasteValues = { ...(host.aiProvidersPasteValues ?? {}), [id]: "" };
        host.aiProvidersRestartNeeded = true;
        await loadAiProviders(host);
      } else {
        host.aiProvidersMessage = { kind: "error", text: result?.error ?? "Failed to store token." };
      }
    } else {
      // API key — use secrets.write (adds to env + vault)
      const envKeyMap: Record<string, string> = {
        anthropic: "ANTHROPIC_API_KEY",
        openai: "OPENAI_API_KEY",
        google: "GOOGLE_API_KEY",
        openrouter: "OPENROUTER_API_KEY",
      };
      const envKey = envKeyMap[id];
      if (!envKey) {
        host.aiProvidersMessage = { kind: "error", text: "Unknown provider." };
        return;
      }
      const result = await host.client.request<{ ok: boolean; masked?: string; restartNeeded?: boolean }>(
        "secrets.write",
        { id: envKey, value, envEntry: true },
      );
      if (result?.ok) {
        host.aiProvidersMessage = { kind: "success", text: `✅ ${provider.name} API key saved securely.` };
        host.aiProvidersActiveConnect = null;
        host.aiProvidersPasteValues = { ...(host.aiProvidersPasteValues ?? {}), [id]: "" };
        if (result.restartNeeded) host.aiProvidersRestartNeeded = true;
        await loadAiProviders(host);
      } else {
        host.aiProvidersMessage = { kind: "error", text: "Failed to save key." };
      }
    }
  } catch (err) {
    host.aiProvidersMessage = { kind: "error", text: `Error: ${err instanceof Error ? err.message : String(err)}` };
  }
}

// ─── OAuth (OpenAI Codex) ─────────────────────────────────────────────────────

export async function aiProvidersOAuth(host: AiProvidersState, id: string): Promise<void> {
  if (!host.client) return;
  host.aiProvidersConnecting = id;
  host.aiProvidersOauthUrl = null;
  host.aiProvidersOauthSessionId = null;
  host.aiProvidersMessage = null;

  try {
    // Step 1: start the flow — gateway returns the auth URL immediately
    const startResult = await host.client.request<{
      ok: boolean;
      sessionId?: string;
      url?: string;
      error?: string;
    }>("auth.login.openai-codex", {});

    if (!startResult?.ok) {
      host.aiProvidersConnecting = null;
      host.aiProvidersMessage = {
        kind: "error",
        text: startResult?.error ?? "Failed to start OAuth. Try again or use an API key.",
      };
      return;
    }

    // Surface the URL in the card so the user can click it (no popup needed)
    host.aiProvidersOauthUrl = startResult.url ?? null;
    host.aiProvidersOauthSessionId = startResult.sessionId ?? null;

    // Step 2: poll for completion (gateway waits for the OAuth callback)
    const pollResult = await host.client.request<{
      ok: boolean;
      profileId?: string;
      email?: string;
      error?: string;
    }>("auth.login.openai-codex.poll", { sessionId: startResult.sessionId });

    host.aiProvidersConnecting = null;
    host.aiProvidersOauthUrl = null;
    host.aiProvidersOauthSessionId = null;

    if (pollResult?.ok) {
      const who = pollResult.email ?? pollResult.profileId ?? "account";
      host.aiProvidersMessage = {
        kind: "success",
        text: `✅ Signed in as ${who} via OpenAI Codex OAuth!`,
      };
      host.aiProvidersActiveConnect = null;
      host.aiProvidersRestartNeeded = true;
      await loadAiProviders(host);
    } else {
      host.aiProvidersMessage = {
        kind: "error",
        text: pollResult?.error ?? "OAuth sign-in failed. Try again or use an API key.",
      };
    }
  } catch (err) {
    host.aiProvidersConnecting = null;
    host.aiProvidersOauthUrl = null;
    host.aiProvidersOauthSessionId = null;
    host.aiProvidersMessage = {
      kind: "error",
      text: `OAuth error: ${err instanceof Error ? err.message : String(err)}`,
    };
  }
}

// ─── Anthropic auto-detect ────────────────────────────────────────────────────

export async function aiProvidersAnthropicAuto(host: AiProvidersState): Promise<void> {
  if (!host.client) return;
  host.aiProvidersConnecting = "anthropic";
  host.aiProvidersMessage = null;
  try {
    const result = await host.client.request<{
      ok: boolean;
      profileId?: string;
      error?: string;
    }>("auth.login.anthropic-auto", {});
    host.aiProvidersConnecting = null;
    if (result?.ok) {
      host.aiProvidersMessage = {
        kind: "success",
        text: `✅ Anthropic token auto-detected from claude CLI and saved! (${result.profileId ?? "anthropic:claude-cli"})`,
      };
      host.aiProvidersActiveConnect = null;
      host.aiProvidersRestartNeeded = true;
      await loadAiProviders(host);
    } else {
      host.aiProvidersMessage = {
        kind: "error",
        text: result?.error ?? "Auto-detect failed.",
      };
    }
  } catch (err) {
    host.aiProvidersConnecting = null;
    host.aiProvidersMessage = {
      kind: "error",
      text: `Auto-detect error: ${err instanceof Error ? err.message : String(err)}`,
    };
  }
}

// ─── OAuth manual redirect paste ─────────────────────────────────────────────

export function aiProvidersOauthPasteChange(host: AiProvidersState, value: string): void {
  host.aiProvidersOauthRedirectPaste = value;
}

export async function aiProvidersSubmitCode(host: AiProvidersState): Promise<void> {
  if (!host.client) return;
  const sessionId = host.aiProvidersOauthSessionId;
  const input = (host.aiProvidersOauthRedirectPaste ?? "").trim();
  if (!sessionId || !input) return;
  try {
    await host.client.request("auth.login.openai-codex.submit-code", { sessionId, input });
    host.aiProvidersOauthRedirectPaste = "";
  } catch (err) {
    host.aiProvidersMessage = {
      kind: "error",
      text: `Failed to submit code: ${err instanceof Error ? err.message : String(err)}`,
    };
  }
}

// ─── Remove profile ───────────────────────────────────────────────────────────

export async function aiProvidersRemoveProfile(
  host: AiProvidersState,
  profileId: string,
): Promise<void> {
  if (!host.client) return;
  try {
    await host.client.request("auth.login.remove", { profileId });
    host.aiProvidersMessage = { kind: "success", text: `Profile removed.` };
    host.aiProvidersRestartNeeded = true;
    await loadAiProviders(host);
  } catch (err) {
    host.aiProvidersMessage = { kind: "error", text: `Failed to remove: ${err instanceof Error ? err.message : String(err)}` };
  }
}
