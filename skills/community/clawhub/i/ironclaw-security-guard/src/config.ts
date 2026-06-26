import os from "node:os";
import path from "node:path";

export type SecurityConfig = {
  enabled: boolean;
  monitorOnly: boolean;
  blockDestructiveShell: boolean;
  protectSensitivePaths: boolean;
  redactSecretsInMessages: boolean;
  networkDenyByDefault: boolean;
  allowedOutboundHosts: string[];
  auditLogPath: string;
  protectedPathPatterns: string[];
  blockedCommandPatterns: string[];
};

const DEFAULT_PROTECTED_PATH_PATTERNS = [
  "\\.env(?:\\.|$)",
  "\\.ssh(?:/|\\\\)",
  "id_rsa",
  "id_ed25519",
  "/etc/shadow",
  "/etc/sudoers",
  "Library/Keychains",
  "\\.openclaw/openclaw\\.json",
  "\\.git/config",
  "\\.npmrc",
  "\\.pypirc",
  "\\.aws/credentials",
];

const DEFAULT_BLOCKED_COMMAND_PATTERNS = [
  "\\brm\\s+-[A-Za-z]*r[A-Za-z]*f\\b",
  "\\bmkfs(?:\\.|\\s)",
  "\\bdd\\s+if=",
  "\\b(?:shutdown|reboot|halt|poweroff)\\b",
  "\\bdiskutil\\s+erase",
  "\\bgit\\s+reset\\s+--hard\\b",
  "\\bgit\\s+clean\\s+-f(?:d|x|dx|fdx)*\\b",
  "\\bchmod\\s+-R\\s+777\\s+/",
  "(?:curl|wget)[^\\n|]*\\|\\s*(?:sh|bash|zsh)\\b",
  "\\bsudo\\b",
  "\\blaunchctl\\s+bootout\\b",
];

function normalizeStringArray(value: unknown, fallback: string[]): string[] {
  if (!Array.isArray(value)) {
    return [...fallback];
  }
  return value
    .map((item) => (typeof item === "string" ? item.trim() : ""))
    .filter(Boolean);
}

export function normalizeSecurityConfig(raw: unknown): SecurityConfig {
  const cfg = raw && typeof raw === "object" ? (raw as Record<string, unknown>) : {};
  return {
    enabled: cfg.enabled !== false,
    monitorOnly: cfg.monitorOnly === true,
    blockDestructiveShell: cfg.blockDestructiveShell !== false,
    protectSensitivePaths: cfg.protectSensitivePaths !== false,
    redactSecretsInMessages: cfg.redactSecretsInMessages !== false,
    networkDenyByDefault: cfg.networkDenyByDefault === true,
    allowedOutboundHosts: normalizeStringArray(cfg.allowedOutboundHosts, ["127.0.0.1", "localhost"]),
    auditLogPath:
      typeof cfg.auditLogPath === "string" && cfg.auditLogPath.trim()
        ? cfg.auditLogPath.trim()
        : path.join(os.homedir(), ".openclaw", "logs", "ironclaw-security-guard.audit.jsonl"),
    protectedPathPatterns: normalizeStringArray(
      cfg.protectedPathPatterns,
      DEFAULT_PROTECTED_PATH_PATTERNS,
    ),
    blockedCommandPatterns: normalizeStringArray(
      cfg.blockedCommandPatterns,
      DEFAULT_BLOCKED_COMMAND_PATTERNS,
    ),
  };
}
