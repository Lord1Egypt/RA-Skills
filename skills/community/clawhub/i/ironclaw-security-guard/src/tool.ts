import type { SecurityConfig } from "./config.ts";
import type { Finding } from "./scan.ts";
import { analyzePayload, redactSecretsInText } from "./scan.ts";

type AuditWriter = {
  write: (event: {
    type: string;
    severity: "low" | "medium" | "high" | "critical";
    findings: Finding[];
    preview?: string;
    toolName?: string;
    blocked?: boolean;
  }) => Promise<void>;
};

export function createSecurityScanTool(params: {
  config: SecurityConfig;
  audit: AuditWriter;
}) {
  return {
    name: "ironclaw_security_scan",
    label: "Security Scan",
    description:
      "Scan content or planned tool parameters for prompt injection, secret leakage, dangerous commands, protected paths, and outbound host risk.",
    parameters: {
      type: "object",
      additionalProperties: false,
      properties: {
        content: {
          type: "string",
          description: "Free-form text or command content to inspect.",
        },
        toolName: {
          type: "string",
          description: "Optional planned tool name for context-aware risk analysis.",
        },
        params: {
          type: "object",
          description: "Optional structured parameters to inspect.",
          additionalProperties: true,
        },
        redactPreview: {
          type: "boolean",
          description: "Whether to include a secret-redacted preview in the result.",
        },
      },
    },
    async execute(_toolCallId: string, rawParams: Record<string, unknown>) {
      const toolName =
        typeof rawParams.toolName === "string" && rawParams.toolName.trim()
          ? rawParams.toolName.trim()
          : "manual-scan";
      const payload = {
        content: typeof rawParams.content === "string" ? rawParams.content : "",
        params:
          rawParams.params && typeof rawParams.params === "object" ? rawParams.params : undefined,
      };

      const report = analyzePayload({
        config: params.config,
        toolName,
        value: payload,
      });

      const previewSource = JSON.stringify(payload, null, 2);
      const preview =
        rawParams.redactPreview === true
          ? redactSecretsInText(previewSource).text
          : undefined;

      await params.audit.write({
        type: "manual_scan",
        severity: report.severity,
        findings: report.findings,
        preview: previewSource.slice(0, 1200),
        toolName,
        blocked: report.block,
      });

      const details = {
        ok: report.findings.length === 0,
        severity: report.severity,
        blockRecommended: report.block,
        findings: report.findings,
        preview,
      };

      return {
        content: [{ type: "text" as const, text: JSON.stringify(details, null, 2) }],
        details,
      };
    },
  };
}
