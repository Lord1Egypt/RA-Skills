import pluginManifest from "../openclaw.plugin.json";
export { ISPConfigError, ISPConfigErrorCode, normalizeError } from "./errors";
import { createTools } from "./tools";
import { ISPConfigPluginConfig, JsonMap } from "./types";

export interface OpenClawRuntimeLike {
  registerTool: (name: string, definition: { description: string; parameters?: Record<string, unknown>; run: (params: JsonMap) => Promise<unknown> }) => void;
}

function ensureConfig(config: Partial<ISPConfigPluginConfig>): ISPConfigPluginConfig {
  if (!config.apiUrl || !config.username || !config.password) {
    throw new Error("Missing required config: apiUrl, username, password");
  }

  return {
    apiUrl: config.apiUrl,
    username: config.username,
    password: config.password,
    serverId: config.serverId ?? 1,
    defaultServerIp: config.defaultServerIp,
    readOnly: config.readOnly ?? false,
    allowedOperations: config.allowedOperations ?? [],
    verifySsl: config.verifySsl ?? true,
    timeoutMs: config.timeoutMs,
  };
}

export interface BoundTool {
  name: string;
  description: string;
  parameters?: {
    type: "object";
    properties: Record<string, unknown>;
    required?: string[];
  };
  run: (params: JsonMap) => Promise<unknown>;
}

export function buildToolset(config: Partial<ISPConfigPluginConfig>): BoundTool[] {
  const safeConfig = ensureConfig(config);
  const context = { config: safeConfig };
  return createTools().map((tool) => ({
    name: tool.name,
    description: tool.description,
    parameters: tool.parameters ?? { type: "object" as const, properties: {} },
    run: (params: JsonMap) => tool.run(params, context),
  }));
}

export function registerAllTools(runtime: OpenClawRuntimeLike, config: Partial<ISPConfigPluginConfig>): void {
  const tools = buildToolset(config);
  for (const tool of tools) {
    runtime.registerTool(tool.name, {
      description: tool.description,
      parameters: tool.parameters,
      run: (params: JsonMap) => tool.run(params),
    });
  }
}

// OpenClaw PluginApi adapter
function registerViaApi(api: any): void {
  const config = (api.pluginConfig ?? {}) as Partial<ISPConfigPluginConfig>;
  const tools = buildToolset(config);
  for (const tool of tools) {
    api.registerTool({
      name: tool.name,
      description: tool.description,
      parameters: tool.parameters,
      execute: (...args: unknown[]) => {
        // OpenClaw may pass (toolCallId, params) or just (params)
        const params = (typeof args[0] === "string" && args.length > 1 ? args[1] : args[0]) as JsonMap ?? {};
        return tool.run(params);
      },
    });
  }

  // Command: /ispconfig - show plugin help
  api.registerCommand({
    name: "ispconfig",
    description: "Show ISPConfig plugin help and list of available tools.",
    usage: "/ispconfig",
    requireAuth: false,
    acceptsArgs: false,
    handler: async () => {
      const rawUrl: string = (config.apiUrl ?? "").trim();
      // Extract hostname only - never expose credentials
      let displayHost = "(not configured)";
      try {
        if (rawUrl) {
          displayHost = new URL(rawUrl).hostname;
        }
      } catch {
        displayHost = rawUrl.replace(/^https?:\/\//, "").split("/")[0] ?? rawUrl;
      }

      const version: string = (pluginManifest as { version?: string }).version ?? "0.3.0";

      const text = [
        `🖥️ *ISPConfig Plugin*`,
        `Version ${version} | Connected to ${displayHost}`,
        ``,
        `📋 *Read (22)*`,
        `• isp_system_info - Server-Info`,
        `• isp_client_list / _get - Clients`,
        `• isp_sites_list / _get - Websites`,
        `• isp_domains_list - Alle Domains`,
        `• isp_dns_zone_list / _get - DNS Zonen`,
        `• isp_dns_record_list - DNS Records (zone_id)`,
        `• isp_mail_domain_list - Mail-Domains`,
        `• isp_mail_user_list - Mail-User`,
        `• isp_mail_alias_list - Mail-Aliase`,
        `• isp_mail_forward_list - Mail-Forwards`,
        `• isp_db_list / _get - Datenbanken`,
        `• isp_db_user_get - DB User Details`,
        `• isp_ftp_user_get - FTP User Details`,
        `• isp_shell_user_get - Shell User Details`,
        `• isp_cron_list - Cron Jobs`,
        `• isp_ssl_status - SSL/LE Status`,
        `• isp_quota_check - Quota (client_id)`,
        `• isp_methods_list - API-Methoden`,
        ``,
        `✏️ *Write (42)*`,
        `• isp_client_add / _update / _delete - Clients`,
        `• isp_site_add / _update / _delete - Websites`,
        `• isp_dns_zone_add / _update / _delete - DNS Zonen`,
        `• isp_dns_record_add / _update / _delete - DNS Records (A, AAAA, MX, TXT, CNAME, SRV, CAA, NS, PTR)`,
        `• isp_mail_domain_add / _update / _delete - Mail-Domains`,
        `• isp_mail_user_add / _update / _delete - Mail-User`,
        `• isp_mail_alias_add / _update / _delete - Mail-Aliase`,
        `• isp_mail_forward_add / _update / _delete - Mail-Forwards`,
        `• isp_db_add / _update / _delete - Datenbanken`,
        `• isp_db_user_add / _update / _delete - DB User`,
        `• isp_ftp_user_add / _update / _delete - FTP User`,
        `• isp_shell_user_add / _update / _delete - Shell User`,
        `• isp_cron_add / _update / _delete - Cron Jobs`,
        ``,
        `🚀 *Provisioning*`,
        `• isp_provision_site - Domain + DNS + Mail + DB in einem Schritt`,
        ``,
        `📝 *Beispiele*`,
        `"Zeig mir alle Websites" -> isp_sites_list`,
        `"DNS Records für Zone 1" -> isp_dns_record_list zone_id=1`,
        `"DNS Zone updaten" -> isp_dns_zone_update client_id=3 primary_id=2 params={ns: "isp.elvatis.com."}`,
        `"Neue Domain anlegen" -> isp_provision_site domain=example.com clientName=Test clientEmail=test@example.com`,
      ].join("\n");

      return { text };
    },
  });
}

const plugin = {
  manifest: pluginManifest,
  register: registerViaApi,
};

export default plugin;
