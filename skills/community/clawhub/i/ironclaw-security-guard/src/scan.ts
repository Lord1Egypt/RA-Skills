import type { SecurityConfig } from "./config.ts";

export type Finding = {
  category: string;
  severity: "low" | "medium" | "high" | "critical";
  message: string;
};

export type ScanReport = {
  severity: "low" | "medium" | "high" | "critical";
  findings: Finding[];
  block: boolean;
};

const SECRET_PATTERNS: Array<{ label: string; regex: RegExp; severity: Finding["severity"] }> = [
  { label: "OpenAI key", regex: /\bsk-[A-Za-z0-9]{20,}\b/g, severity: "critical" },
  { label: "GitHub token", regex: /\bgh[pousr]_[A-Za-z0-9]{20,}\b/g, severity: "critical" },
  { label: "Slack token", regex: /\bxox[baprs]-[A-Za-z0-9-]{10,}\b/g, severity: "critical" },
  { label: "Google API key", regex: /\bAIza[0-9A-Za-z\-_]{35}\b/g, severity: "critical" },
  { label: "AWS access key", regex: /\bAKIA[0-9A-Z]{16}\b/g, severity: "critical" },
  { label: "Private key block", regex: /-----BEGIN [A-Z ]*PRIVATE KEY-----/g, severity: "critical" },
  { label: "Bearer token", regex: /\bBearer\s+[A-Za-z0-9._\-]{20,}\b/g, severity: "high" },
];

const INJECTION_PATTERNS: Array<{ label: string; regex: RegExp; severity: Finding["severity"] }> = [
  {
    label: "ignore instructions",
    regex: /\bignore\s+(all|any|the)?\s*(previous|prior|above)\s+(instructions|system|rules?)\b/gi,
    severity: "high",
  },
  {
    label: "reveal system prompt",
    regex: /\b(reveal|show|print|dump)\s+(the\s+)?(system prompt|developer message|hidden prompt)\b/gi,
    severity: "high",
  },
  {
    label: "tool exfiltration prompt",
    regex: /\b(send|post|upload|exfiltrat(?:e|ion))\b.{0,80}\b(secret|token|credential|password)\b/gi,
    severity: "critical",
  },
  {
    label: "override behavior",
    regex: /\byou are now\b|\bnew instructions\b|\bforget your role\b/gi,
    severity: "medium",
  },
];

const URL_REGEX = /\bhttps?:\/\/[^\s"'`<>]+/gi;
const PATH_TRAVERSAL_REGEX = /(^|[\s"'`])\.\.(?:\/|\\)/g;

function matchesRegex(text: string, regex: RegExp): boolean {
  regex.lastIndex = 0;
  return regex.test(text);
}

function extractStrings(value: unknown, out: string[] = []): string[] {
  if (typeof value === "string") {
    out.push(value);
    return out;
  }
  if (Array.isArray(value)) {
    for (const item of value) {
      extractStrings(item, out);
    }
    return out;
  }
  if (value && typeof value === "object") {
    for (const item of Object.values(value as Record<string, unknown>)) {
      extractStrings(item, out);
    }
  }
  return out;
}

function highestSeverity(findings: Finding[]): Finding["severity"] {
  const rank: Record<Finding["severity"], number> = {
    low: 0,
    medium: 1,
    high: 2,
    critical: 3,
  };
  return findings.reduce<Finding["severity"]>(
    (max, finding) => (rank[finding.severity] > rank[max] ? finding.severity : max),
    "low",
  );
}

function hostFromUrl(rawUrl: string): string | null {
  try {
    return new URL(rawUrl).hostname.toLowerCase();
  } catch {
    return null;
  }
}

export function classifyTool(toolName: string): "shell" | "network" | "message" | "file" | "other" {
  const name = toolName.toLowerCase();
  if (/(bash|shell|terminal|exec|command|ssh|codex)/.test(name)) {
    return "shell";
  }
  if (/(web|http|fetch|browser|url|request)/.test(name)) {
    return "network";
  }
  if (/(message|mail|email|sms|telegram|discord|slack|feishu|whatsapp|signal|imessage|line|zalo|phone|voice)/.test(name)) {
    return "message";
  }
  if (/(write|edit|patch|file|fs|docx|pdf|ppt|sheet|spreadsheet)/.test(name)) {
    return "file";
  }
  return "other";
}

function matchRegexList(text: string, patterns: string[], category: string): Finding[] {
  const findings: Finding[] = [];
  for (const pattern of patterns) {
    let regex: RegExp;
    try {
      regex = new RegExp(pattern, "i");
    } catch {
      continue;
    }
    if (regex.test(text)) {
      findings.push({
        category,
        severity: category === "destructive-command" ? "critical" : "high",
        message: `Matched ${category} rule: ${pattern}`,
      });
    }
  }
  return findings;
}

function matchProtectedPaths(text: string, config: SecurityConfig): Finding[] {
  if (!config.protectSensitivePaths) {
    return [];
  }
  const findings = matchRegexList(text, config.protectedPathPatterns, "protected-path");
  if (matchesRegex(text, PATH_TRAVERSAL_REGEX)) {
    findings.push({
      category: "path-traversal",
      severity: "high",
      message: "Detected path traversal pattern (`../` or `..\\`).",
    });
  }
  return findings;
}

function matchSecrets(text: string): Finding[] {
  const findings: Finding[] = [];
  for (const pattern of SECRET_PATTERNS) {
    if (matchesRegex(text, pattern.regex)) {
      findings.push({
        category: "secret",
        severity: pattern.severity,
        message: `Detected ${pattern.label}.`,
      });
    }
  }
  return findings;
}

function matchInjection(text: string): Finding[] {
  const findings: Finding[] = [];
  for (const pattern of INJECTION_PATTERNS) {
    if (matchesRegex(text, pattern.regex)) {
      findings.push({
        category: "prompt-injection",
        severity: pattern.severity,
        message: `Detected ${pattern.label} pattern.`,
      });
    }
  }
  return findings;
}

function checkUrls(text: string, config: SecurityConfig): Finding[] {
  const findings: Finding[] = [];
  const urls = text.match(URL_REGEX) ?? [];
  for (const url of urls) {
    const host = hostFromUrl(url);
    if (!host) {
      continue;
    }
    const allowed = config.allowedOutboundHosts.some((item) => {
      const normalized = item.toLowerCase();
      return host === normalized || host.endsWith(`.${normalized}`);
    });
    if (config.networkDenyByDefault && !allowed) {
      findings.push({
        category: "network-allowlist",
        severity: "high",
        message: `Host not on allowlist: ${host}`,
      });
    }
  }
  return findings;
}

export function analyzePayload(params: {
  config: SecurityConfig;
  toolName: string;
  value: unknown;
}): ScanReport {
  const findings: Finding[] = [];
  const toolClass = classifyTool(params.toolName);
  const strings = extractStrings(params.value);
  const joined = strings.join("\n");

  findings.push(...matchInjection(joined));
  findings.push(...matchProtectedPaths(joined, params.config));
  findings.push(...checkUrls(joined, params.config));

  if (toolClass === "shell" && params.config.blockDestructiveShell) {
    findings.push(
      ...matchRegexList(joined, params.config.blockedCommandPatterns, "destructive-command"),
    );
  }

  if (toolClass === "network" || toolClass === "message") {
    findings.push(...matchSecrets(joined));
  }

  if (toolClass === "file" || toolClass === "shell") {
    findings.push(...matchSecrets(joined));
  }

  const severity = highestSeverity(findings);
  const block =
    findings.some((finding) => finding.category === "destructive-command") ||
    findings.some((finding) => finding.category === "protected-path") ||
    findings.some((finding) => finding.category === "path-traversal") ||
    ((toolClass === "network" || toolClass === "message") &&
      findings.some((finding) => finding.category === "secret"));

  return {
    severity,
    findings,
    block,
  };
}

export function redactSecretsInText(text: string): {
  text: string;
  changed: boolean;
  findings: Finding[];
} {
  let output = text;
  const findings: Finding[] = [];
  for (const pattern of SECRET_PATTERNS) {
    if (matchesRegex(output, pattern.regex)) {
      pattern.regex.lastIndex = 0;
      output = output.replace(pattern.regex, `[REDACTED:${pattern.label}]`);
      findings.push({
        category: "secret-redaction",
        severity: pattern.severity,
        message: `Redacted ${pattern.label}.`,
      });
    }
  }
  return {
    text: output,
    changed: output !== text,
    findings,
  };
}

export function buildBlockedToolReason(toolName: string, findings: Finding[]): string {
  const top = findings
    .slice(0, 3)
    .map((finding) => `${finding.category}: ${finding.message}`)
    .join("; ");
  return `Blocked by ironclaw-security-guard before calling ${toolName}. ${top}`;
}
