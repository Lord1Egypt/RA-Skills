import type { OpenClawPluginApi } from "openclaw/plugin-sdk/core";
import { createAuditLogger } from "./src/audit.ts";
import { normalizeSecurityConfig } from "./src/config.ts";
import { SECURITY_PROMPT_GUIDANCE } from "./src/prompt-guidance.ts";
import {
  analyzePayload,
  buildBlockedToolReason,
  classifyTool,
  redactSecretsInText,
} from "./src/scan.ts";
import { createSecurityScanTool } from "./src/tool.ts";

const plugin = {
  id: "ironclaw-security-guard",
  name: "IronClaw Security Guard",
  description:
    "Defense-in-depth security guard for OpenClaw inspired by IronClaw patterns.",
  register(api: OpenClawPluginApi) {
    const config = normalizeSecurityConfig(api.pluginConfig);
    const audit = createAuditLogger(config.auditLogPath, api.logger);

    api.registerTool(createSecurityScanTool({ config, audit }));

    api.on("before_prompt_build", async () => {
      if (!config.enabled) {
        return;
      }
      return {
        prependSystemContext: SECURITY_PROMPT_GUIDANCE,
      };
    });

    api.on("message_received", async (event, ctx) => {
      if (!config.enabled) {
        return;
      }
      const report = analyzePayload({
        config,
        toolName: "message_received",
        value: { content: event.content },
      });
      if (report.severity === "high" || report.severity === "critical") {
        await audit.write({
          type: "message_received",
          severity: report.severity,
          sessionKey: ctx.sessionKey,
          agentId: ctx.agentId,
          runId: undefined,
          findings: report.findings,
          preview: String(event.content ?? "").slice(0, 800),
        });
      }
    });

    api.on("before_tool_call", async (event, ctx) => {
      if (!config.enabled) {
        return;
      }
      const report = analyzePayload({
        config,
        toolName: event.toolName,
        value: event.params,
      });

      const shouldBlock =
        !config.monitorOnly &&
        (report.block || report.severity === "critical" || report.severity === "high");

      if (report.findings.length > 0) {
        await audit.write({
          type: "before_tool_call",
          severity: report.severity,
          sessionKey: ctx.sessionKey,
          agentId: ctx.agentId,
          runId: event.runId,
          toolName: event.toolName,
          findings: report.findings,
          preview: JSON.stringify(event.params).slice(0, 1200),
          blocked: shouldBlock,
        });
      }

      if (shouldBlock) {
        return {
          block: true,
          blockReason: buildBlockedToolReason(event.toolName, report.findings),
        };
      }
    });

    api.on("message_sending", async (event, ctx) => {
      if (!config.enabled || !config.redactSecretsInMessages) {
        return;
      }
      const redaction = redactSecretsInText(event.content);
      if (!redaction.changed) {
        return;
      }
      await audit.write({
        type: "message_sending",
        severity: "high",
        sessionKey: ctx.sessionKey,
        agentId: ctx.agentId,
        findings: redaction.findings,
        preview: event.content.slice(0, 1200),
        blocked: false,
      });
      return {
        content: `${redaction.text}\n\n[security] Sensitive-looking tokens were redacted before sending.`,
      };
    });

    api.on("after_tool_call", async (event, ctx) => {
      if (!config.enabled || event.error == null) {
        return;
      }
      const toolClass = classifyTool(event.toolName);
      if (toolClass === "shell" || toolClass === "network" || toolClass === "message") {
        await audit.write({
          type: "after_tool_call",
          severity: "medium",
          sessionKey: ctx.sessionKey,
          agentId: ctx.agentId,
          runId: event.runId,
          toolName: event.toolName,
          findings: [
            {
              category: "tool-error",
              severity: "medium",
              message: String(event.error),
            },
          ],
          preview: JSON.stringify(event.params).slice(0, 1200),
        });
      }
    });
  },
};

export default plugin;
