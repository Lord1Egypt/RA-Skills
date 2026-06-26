/**
 * Environment variables for this skill use the POWERLOOM_* prefix only (see SKILL.md).
 */

function env(name) {
  const v = process.env[name];
  if (v === undefined || v === null || String(v).trim() === "") return "";
  return String(v).trim();
}

export function meteringBaseUrl() {
  return (env("POWERLOOM_METERING_BASE_URL") || "https://bds-metering.powerloom.io").replace(
    /\/$/,
    "",
  );
}

export function evmPrivateKey() {
  return env("POWERLOOM_EVM_PRIVATE_KEY");
}

export function evmRpcUrl() {
  return env("POWERLOOM_EVM_RPC_URL");
}

export function planId() {
  return env("POWERLOOM_PLAN_ID");
}

export function tokenSymbol() {
  return env("POWERLOOM_TOKEN_SYMBOL");
}

export function chainIdParsed() {
  return parseInt(env("POWERLOOM_EVM_CHAIN_ID"), 10);
}

export function agentNameOr(defaultName) {
  return env("POWERLOOM_AGENT_NAME") || defaultName;
}

export function signupEmail() {
  return env("POWERLOOM_EMAIL");
}

export function powerloomApiKey() {
  return env("POWERLOOM_API_KEY");
}

export function telegramBotToken() {
  return env("POWERLOOM_TELEGRAM_BOT_TOKEN");
}

export function telegramChatId() {
  return env("POWERLOOM_TELEGRAM_CHAT_ID");
}

export function discordWebhookUrl() {
  return env("POWERLOOM_DISCORD_WEBHOOK_URL");
}

/** If POWERLOOM_BDS_MCP_CALL_TIMEOUT_MS is unset, set it (ms) so MCP clients pick up the recipe/script default. */
export function defaultMcpCallTimeoutIfUnset(ms) {
  if (!env("POWERLOOM_BDS_MCP_CALL_TIMEOUT_MS")) {
    process.env.POWERLOOM_BDS_MCP_CALL_TIMEOUT_MS = String(ms);
  }
}

export function mcpDebugEnabled() {
  return env("POWERLOOM_BDS_MCP_DEBUG") === "1";
}
