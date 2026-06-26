import { ISPConfigClient } from "./client";
import { normalizeError } from "./errors";
import { assertToolAllowed } from "./guards";
import { JsonMap, ToolContext, ToolDefinition } from "./types";
import { validateParams } from "./validate";

const KNOWN_METHODS = [
  "server_get_all", "server_get", "client_get_all", "client_get", "client_add", "client_update", "client_delete",
  "sites_web_domain_get", "sites_web_domain_add", "sites_web_domain_update", "sites_web_domain_delete",
  "dns_zone_get_by_user", "dns_zone_get", "dns_zone_add", "dns_zone_update", "dns_zone_delete", "dns_rr_get_all_by_zone",
  "dns_a_add", "dns_aaaa_add", "dns_mx_add", "dns_txt_add", "dns_cname_add",
  "dns_a_delete", "dns_aaaa_delete", "dns_mx_delete", "dns_txt_delete", "dns_cname_delete",
  "dns_a_update", "dns_aaaa_update", "dns_mx_update", "dns_txt_update", "dns_cname_update",
  "dns_srv_add", "dns_srv_update", "dns_srv_delete",
  "dns_caa_add", "dns_caa_update", "dns_caa_delete",
  "dns_ns_add", "dns_ns_update", "dns_ns_delete",
  "dns_ptr_add", "dns_ptr_update", "dns_ptr_delete",
  "mail_domain_get", "mail_domain_add", "mail_domain_update", "mail_domain_delete",
  "mail_user_get", "mail_user_add", "mail_user_update", "mail_user_delete",
  "mail_alias_get", "mail_alias_add", "mail_alias_update", "mail_alias_delete",
  "mail_forward_get", "mail_forward_add", "mail_forward_update", "mail_forward_delete",
  "sites_database_get_all_by_user", "sites_database_get", "sites_database_add", "sites_database_update", "sites_database_delete",
  "sites_database_user_get", "sites_database_user_add", "sites_database_user_update", "sites_database_user_delete",
  "sites_shell_user_get", "sites_shell_user_add", "sites_shell_user_update", "sites_shell_user_delete",
  "sites_ftp_user_get", "sites_ftp_user_add", "sites_ftp_user_update", "sites_ftp_user_delete",
  "sites_cron_get", "sites_cron_add", "sites_cron_delete", "sites_cron_update",
  // Phase 1: Core Completion
  "client_get_id", "client_get_emailcontact", "client_get_groupid",
  "client_get_by_username", "client_get_by_customer_no", "client_get_by_groupid",
  "client_get_sites_by_user", "client_change_password", "client_delete_everything",
  "client_login_get", "client_template_additional_get", "client_template_additional_add",
  "client_template_additional_delete", "client_templates_get_all",
  "server_get_app_version", "server_get_functions", "server_get_php_versions",
  "server_get_serverid_by_ip", "server_get_serverid_by_name",
  "server_ip_get", "server_ip_add", "server_ip_update", "server_ip_delete", "server_config_set",
  "sites_web_domain_backup", "sites_web_domain_backup_list", "sites_web_domain_set_status",
  "quota_get_by_user", "trafficquota_get_by_user", "ftptrafficquota_data", "databasequota_get_by_user",
  "monitor_jobqueue_count",
  // Phase 2: DNS Complete
  "dns_a_get", "dns_aaaa_get", "dns_caa_get", "dns_cname_get", "dns_mx_get",
  "dns_ns_get", "dns_ptr_get", "dns_srv_get", "dns_txt_get",
  "dns_alias_get", "dns_alias_add", "dns_alias_update", "dns_alias_delete",
  "dns_dname_get", "dns_dname_add", "dns_dname_update", "dns_dname_delete",
  "dns_ds_get", "dns_ds_add", "dns_ds_update", "dns_ds_delete",
  "dns_hinfo_get", "dns_hinfo_add", "dns_hinfo_update", "dns_hinfo_delete",
  "dns_loc_get", "dns_loc_add", "dns_loc_update", "dns_loc_delete",
  "dns_naptr_get", "dns_naptr_add", "dns_naptr_update", "dns_naptr_delete",
  "dns_rp_get", "dns_rp_add", "dns_rp_update", "dns_rp_delete",
  "dns_sshfp_get", "dns_sshfp_add", "dns_sshfp_update", "dns_sshfp_delete",
  "dns_tlsa_get", "dns_tlsa_add", "dns_tlsa_update", "dns_tlsa_delete",
  "dns_slave_get", "dns_slave_add", "dns_slave_update", "dns_slave_delete",
  "dns_templatezone_get_all", "dns_templatezone_add",
  "dns_zone_get_id", "dns_zone_set_status", "dns_zone_set_dnssec",
  // Phase 3: Mail Complete
  "mail_aliasdomain_get", "mail_aliasdomain_add", "mail_aliasdomain_update", "mail_aliasdomain_delete",
  "mail_catchall_get", "mail_catchall_add", "mail_catchall_update", "mail_catchall_delete",
  "mail_mailinglist_get", "mail_mailinglist_add", "mail_mailinglist_update", "mail_mailinglist_delete",
  "mail_user_filter_get", "mail_user_filter_add", "mail_user_filter_update", "mail_user_filter_delete",
  "mail_user_backup_list", "mail_user_backup", "mail_user_get_all_by_client",
  "mail_domain_get_by_domain", "mail_domain_set_status",
  "mailquota_get_by_user",
  "mail_fetchmail_get", "mail_fetchmail_add", "mail_fetchmail_update", "mail_fetchmail_delete",
  "mail_transport_get", "mail_transport_add", "mail_transport_update", "mail_transport_delete",
  "mail_relay_recipient_get", "mail_relay_recipient_add", "mail_relay_recipient_update", "mail_relay_recipient_delete",
  "mail_relay_domain_get", "mail_relay_domain_add", "mail_relay_domain_update", "mail_relay_domain_delete",
  "mail_spamfilter_whitelist_get", "mail_spamfilter_whitelist_add", "mail_spamfilter_whitelist_update", "mail_spamfilter_whitelist_delete",
  "mail_spamfilter_blacklist_get", "mail_spamfilter_blacklist_add", "mail_spamfilter_blacklist_update", "mail_spamfilter_blacklist_delete",
  "mail_spamfilter_user_get", "mail_spamfilter_user_add", "mail_spamfilter_user_update", "mail_spamfilter_user_delete",
  "mail_policy_get", "mail_policy_add", "mail_policy_update", "mail_policy_delete",
  "mail_whitelist_get", "mail_whitelist_add", "mail_whitelist_update", "mail_whitelist_delete",
  "mail_blacklist_get", "mail_blacklist_add", "mail_blacklist_update", "mail_blacklist_delete",
  "mail_filter_get", "mail_filter_add", "mail_filter_update", "mail_filter_delete",
  // Phase 4: Web Extended
  "sites_web_vhost_aliasdomain_get", "sites_web_vhost_aliasdomain_add", "sites_web_vhost_aliasdomain_update", "sites_web_vhost_aliasdomain_delete",
  "sites_web_vhost_subdomain_get", "sites_web_vhost_subdomain_add", "sites_web_vhost_subdomain_update", "sites_web_vhost_subdomain_delete",
  "sites_web_aliasdomain_get", "sites_web_aliasdomain_add", "sites_web_aliasdomain_update", "sites_web_aliasdomain_delete",
  "sites_web_subdomain_get", "sites_web_subdomain_add", "sites_web_subdomain_update", "sites_web_subdomain_delete",
  "sites_web_folder_get", "sites_web_folder_add", "sites_web_folder_update", "sites_web_folder_delete",
  "sites_web_folder_user_get", "sites_web_folder_user_add", "sites_web_folder_user_update", "sites_web_folder_user_delete",
  "sites_webdav_user_get", "sites_webdav_user_add", "sites_webdav_user_update", "sites_webdav_user_delete",
  "sites_ftp_user_server_get",
  // Phase 5: System & Advanced
  "system_config_get", "system_config_set",
  "config_value_get", "config_value_add", "config_value_update", "config_value_replace", "config_value_delete",
  "sys_datalog_get", "sys_datalog_get_by_tstamp",
  "sites_aps_available_packages_list", "sites_aps_get_package_details", "sites_aps_get_package_file",
  "sites_aps_get_package_settings", "sites_aps_update_package_list", "sites_aps_change_package_status",
  "sites_aps_install_package", "sites_aps_instance_get", "sites_aps_instance_settings_get", "sites_aps_instance_delete",
  "domains_domain_get", "domains_domain_add", "domains_domain_update", "domains_domain_delete", "domains_get_all_by_user",
  "update_record_permissions",
  // Phase 6: OpenVZ Legacy
  "openvz_ostemplate_get", "openvz_ostemplate_add", "openvz_ostemplate_update", "openvz_ostemplate_delete",
  "openvz_template_get", "openvz_template_add", "openvz_template_update", "openvz_template_delete",
  "openvz_ip_get", "openvz_get_free_ip", "openvz_ip_add", "openvz_ip_update", "openvz_ip_delete",
  "openvz_vm_get", "openvz_vm_get_by_client", "openvz_vm_add", "openvz_vm_add_from_template",
  "openvz_vm_update", "openvz_vm_delete", "openvz_vm_start", "openvz_vm_stop", "openvz_vm_restart",
];

function toNumber(value: unknown, fallback?: number): number {
  const n = Number(value);
  if (Number.isFinite(n)) {
    return n;
  }
  if (fallback === undefined) {
    throw new Error(`Expected numeric value, got ${String(value)}`);
  }
  return fallback;
}

function dnsMethodForType(type: string, action: "add" | "delete" | "update"): string {
  switch (type.toUpperCase()) {
    case "A": return `dns_a_${action}`;
    case "AAAA": return `dns_aaaa_${action}`;
    case "MX": return `dns_mx_${action}`;
    case "TXT": return `dns_txt_${action}`;
    case "CNAME": return `dns_cname_${action}`;
    case "SRV": return `dns_srv_${action}`;
    case "CAA": return `dns_caa_${action}`;
    case "NS": return `dns_ns_${action}`;
    case "PTR": return `dns_ptr_${action}`;
    case "DNAME": return `dns_dname_${action}`;
    case "DS": return `dns_ds_${action}`;
    case "HINFO": return `dns_hinfo_${action}`;
    case "LOC": return `dns_loc_${action}`;
    case "NAPTR": return `dns_naptr_${action}`;
    case "RP": return `dns_rp_${action}`;
    case "SSHFP": return `dns_sshfp_${action}`;
    case "TLSA": return `dns_tlsa_${action}`;
    case "ALIAS": return `dns_alias_${action}`;
    default: throw new Error(`Unsupported DNS record type: ${type}`);
  }
}

const DNS_RECORD_TYPES = ["A", "AAAA", "MX", "TXT", "CNAME", "SRV", "CAA", "NS", "PTR", "DNAME", "DS", "HINFO", "LOC", "NAPTR", "RP", "SSHFP", "TLSA", "ALIAS"];

async function withClient<T>(context: ToolContext, toolName: string, fn: (client: ISPConfigClient) => Promise<T>): Promise<T> {
  assertToolAllowed(context.config, toolName);
  const client = new ISPConfigClient(context.config);
  try {
    return await fn(client);
  } finally {
    await client.logout();
  }
}

async function fetchSites(client: ISPConfigClient): Promise<JsonMap[]> {
  const direct = await client.call<JsonMap[]>("sites_web_domain_get", {});
  if (Array.isArray(direct) && direct.length > 0) {
    return direct;
  }

  const fallback: JsonMap[] = [];
  for (let id = 1; id <= 100; id += 1) {
    try {
      const site = await client.call<JsonMap>("sites_web_domain_get", { primary_id: id });
      if (site && typeof site === "object" && site.domain) {
        fallback.push(site);
      }
    } catch {
      // ignore gaps and permission misses
    }
  }
  return fallback;
}

export function createTools(): ToolDefinition[] {
  const raw: ToolDefinition[] = [
    {
      name: "isp_methods_list",
      description: "Discover available ISPConfig API methods (dynamic via get_function_list, falls back to probing known methods)",
      parameters: { type: "object", properties: {} },
      run: async (_params, context) => withClient(context, "isp_methods_list", async (client) => {
        // Try dynamic discovery first (ISPConfig 3.2+)
        try {
          const functions = await client.call<string[]>("get_function_list", {});
          if (Array.isArray(functions) && functions.length > 0) {
            const dynamicSet = new Set(functions);
            const knownAvailable = KNOWN_METHODS.filter((m) => dynamicSet.has(m));
            const knownUnavailable = KNOWN_METHODS.filter((m) => !dynamicSet.has(m));
            const extra = functions.filter((m) => !KNOWN_METHODS.includes(m));
            return {
              discovery: "dynamic",
              available: knownAvailable,
              unavailable: knownUnavailable.map((m) => ({ method: m, reason: "not in get_function_list" })),
              extra,
              totalServer: functions.length,
              totalKnown: KNOWN_METHODS.length,
            };
          }
        } catch {
          // get_function_list not available - fall back to probing
        }

        // Fallback: probe each known method individually
        const available: string[] = [];
        const unavailable: Array<{ method: string; reason: string }> = [];

        for (const method of KNOWN_METHODS) {
          try {
            await client.call(method, {});
            available.push(method);
          } catch (error) {
            const msg = error instanceof Error ? error.message : String(error);
            if (msg.toLowerCase().includes("unknown") || msg.toLowerCase().includes("invalid function")) {
              unavailable.push({ method, reason: msg });
            } else {
              available.push(method);
            }
          }
        }

        return { discovery: "probe", available, unavailable, extra: [], totalServer: 0, totalKnown: KNOWN_METHODS.length };
      }),
    },
    {
      name: "isp_system_info",
      description: "Get ISPConfig server list and server details",
      parameters: { type: "object", properties: {} },
      run: async (_params, context) => withClient(context, "isp_system_info", async (client) => {
        const servers = await client.call<Array<JsonMap>>("server_get_all", {});
        const details: JsonMap[] = [];
        for (const server of servers ?? []) {
          const id = toNumber(server.server_id ?? server.serverid ?? 0, 0);
          if (id > 0) {
            details.push(await client.call<JsonMap>("server_get", { server_id: id }));
          }
        }
        return { servers, details };
      }),
    },
    {
      name: "isp_provision_site",
      description: "Provision client, site, DNS, mail and database in one workflow",
      parameters: {
        type: "object",
        properties: {
          domain: { type: "string", description: "Domain name to provision" },
          clientName: { type: "string", description: "Client company/contact name" },
          clientEmail: { type: "string", description: "Client email address" },
          serverIp: { type: "string", description: "Server IP address for DNS A record" },
          createMail: { type: "boolean", description: "Whether to create mail domain and users (default: true)" },
          createDb: { type: "boolean", description: "Whether to create a database and user (default: true)" },
          serverId: { type: "number", description: "ISPConfig server ID (default: 1)" },
        },
        required: ["domain", "clientName", "clientEmail"],
      },
      run: async (params, context) => withClient(context, "isp_provision_site", async (client) => {
        const domain = String(params.domain ?? "").trim();
        const clientName = String(params.clientName ?? "").trim();
        const clientEmail = String(params.clientEmail ?? "").trim();
        const serverIp = String(params.serverIp ?? context.config.defaultServerIp ?? "").trim();
        const createMail = Boolean(params.createMail ?? true);
        const createDb = Boolean(params.createDb ?? true);
        const serverId = toNumber(params.serverId ?? context.config.serverId ?? 1, 1);

        if (!domain || !clientName || !clientEmail) {
          throw new Error("domain, clientName and clientEmail are required");
        }

        const created: JsonMap = {};

        const newClientId = await client.call<number>("client_add", {
          reseller_id: 0,
          params: { company_name: clientName, contact_name: clientName, email: clientEmail },
        });
        created.client_id = newClientId;

        const websiteId = await client.call<number>("sites_web_domain_add", {
          client_id: newClientId,
          params: {
            server_id: serverId,
            ip_address: "*",
            domain,
            type: "vhost",
            active: "y",
            system_user: `web${newClientId}`,
            system_group: `client${newClientId}`,
            php: "php-fpm",
            ssl: "y",
            ssl_letsencrypt: "y",
          },
        });
        created.site_id = websiteId;

        const zoneId = await client.call<number>("dns_zone_add", {
          client_id: newClientId,
          params: {
            server_id: serverId,
            origin: `${domain}.`,
            ns: `ns1.${domain}.`,
            mbox: `hostmaster.${domain}.`,
            active: "Y",
          },
        });
        created.dns_zone_id = zoneId;

        if (serverIp) {
          await client.call("dns_a_add", { client_id: newClientId, params: { zone: zoneId, name: `${domain}.`, data: serverIp, ttl: 3600, active: "Y" } });
          await client.call("dns_cname_add", { client_id: newClientId, params: { zone: zoneId, name: `www.${domain}.`, data: `${domain}.`, ttl: 3600, active: "Y" } });
        }

        await client.call("dns_txt_add", { client_id: newClientId, params: { zone: zoneId, name: `${domain}.`, data: "v=spf1 mx a ~all", ttl: 3600, active: "Y" } });
        await client.call("dns_txt_add", { client_id: newClientId, params: { zone: zoneId, name: `_dmarc.${domain}.`, data: `v=DMARC1; p=none; rua=mailto:postmaster@${domain}`, ttl: 3600, active: "Y" } });

        if (createMail) {
          const mailDomainId = await client.call<number>("mail_domain_add", { client_id: newClientId, params: { server_id: serverId, domain, active: "y" } });
          created.mail_domain_id = mailDomainId;
          await client.call("mail_user_add", { client_id: newClientId, params: { server_id: serverId, login: `info@${domain}`, email: `info@${domain}`, password: `Temp!${Date.now()}` } });
          await client.call("mail_user_add", { client_id: newClientId, params: { server_id: serverId, login: `admin@${domain}`, email: `admin@${domain}`, password: `Temp!${Date.now()}A` } });
        }

        if (createDb) {
          const dbUserId = await client.call<number>("sites_database_user_add", {
            client_id: newClientId,
            params: { server_id: serverId, database_user: `u${newClientId}_${domain.replace(/\W+/g, "").slice(0, 10)}`, database_password: `Temp!${Date.now()}Db` },
          });
          const dbId = await client.call<number>("sites_database_add", {
            client_id: newClientId,
            params: {
              server_id: serverId,
              database_name: `c${newClientId}_${domain.replace(/\W+/g, "").slice(0, 10)}`,
              database_user_id: dbUserId,
              database_charset: "UTF8",
              remote_access: "n",
              active: "y",
            },
          });
          created.database_user_id = dbUserId;
          created.database_id = dbId;
        }

        await client.call("sites_web_domain_update", { client_id: newClientId, primary_id: websiteId, params: { ssl: "y", ssl_letsencrypt: "y" } });

        return { ok: true, domain, created };
      }),
    },
    {
      name: "isp_client_list",
      description: "List clients with details",
      parameters: { type: "object", properties: {} },
      run: async (_params, context) => withClient(context, "isp_client_list", async (client) => {
        const clients = await client.call<Array<JsonMap>>("client_get_all", {});
        const details: JsonMap[] = [];
        for (const c of clients ?? []) {
          const id = toNumber(c.client_id ?? 0, 0);
          if (id > 0) details.push(await client.call<JsonMap>("client_get", { client_id: id }));
        }
        return { total: clients?.length ?? 0, clients: details };
      }),
    },
    {
      name: "isp_client_add",
      description: "Create a new ISPConfig client",
      parameters: {
        type: "object",
        properties: {
          company_name: { type: "string", description: "Client company name" },
          contact_name: { type: "string", description: "Contact person name" },
          email: { type: "string", description: "Client email address" },
        },
      },
      run: async (params, context) => withClient(context, "isp_client_add", (client) => client.call("client_add", { reseller_id: 0, params })),
    },
    {
      name: "isp_client_get",
      description: "Get client details by client_id",
      parameters: {
        type: "object",
        properties: {
          client_id: { type: "number", description: "Client ID" },
        },
        required: ["client_id"],
      },
      run: async (params, context) => withClient(context, "isp_client_get", (client) => client.call("client_get", { client_id: toNumber(params.client_id ?? params.clientId) })),
    },
    {
      name: "isp_sites_list",
      description: "List web sites with optional filters",
      parameters: { type: "object", properties: {} },
      run: async (params, context) => withClient(context, "isp_sites_list", async (client) => {
        if (Object.keys(params).length > 0) {
          return client.call("sites_web_domain_get", params);
        }
        return fetchSites(client);
      }),
    },
    {
      name: "isp_site_get",
      description: "Get one site by primary_id",
      parameters: {
        type: "object",
        properties: {
          primary_id: { type: "number", description: "Site ID" },
          domain_id: { type: "number", description: "Alias for primary_id" },
          site_id: { type: "number", description: "Alias for primary_id" },
        },
      },
      run: async (params, context) => withClient(context, "isp_site_get", (client) => client.call("sites_web_domain_get", { primary_id: toNumber(params.primary_id ?? params.domain_id ?? params.site_id) })),
    },
    {
      name: "isp_site_add",
      description: "Create web site",
      parameters: {
        type: "object",
        properties: {
          client_id: { type: "number", description: "Client ID" },
          params: { type: "object", description: "Site parameters" },
        },
        required: ["client_id", "params"],
      },
      run: async (params, context) => withClient(context, "isp_site_add", (client) => client.call("sites_web_domain_add", params)),
    },
    {
      name: "isp_domains_list",
      description: "List all web domains",
      parameters: { type: "object", properties: {} },
      run: async (_params, context) => withClient(context, "isp_domains_list", async (client) => {
        const sites = await fetchSites(client);
        return sites.map((s) => ({ domain_id: s.domain_id, domain: s.domain, active: s.active }));
      }),
    },
    {
      name: "isp_domain_add",
      description: "Alias for isp_site_add",
      parameters: {
        type: "object",
        properties: {
          client_id: { type: "number", description: "Client ID" },
          params: { type: "object", description: "Domain/site parameters" },
        },
        required: ["client_id", "params"],
      },
      run: async (params, context) => withClient(context, "isp_domain_add", (client) => client.call("sites_web_domain_add", params)),
    },
    {
      name: "isp_dns_zone_list",
      description: "List DNS zones by user",
      parameters: { type: "object", properties: {} },
      run: async (params, context) => withClient(context, "isp_dns_zone_list", (client) => client.call("dns_zone_get_by_user", params)),
    },
    {
      name: "isp_dns_zone_add",
      description: "Create DNS zone",
      parameters: {
        type: "object",
        properties: {
          client_id: { type: "number", description: "Client ID" },
          params: { type: "object", description: "DNS zone parameters" },
        },
        required: ["client_id", "params"],
      },
      run: async (params, context) => withClient(context, "isp_dns_zone_add", (client) => client.call("dns_zone_add", params)),
    },
    {
      name: "isp_dns_record_list",
      description: "List DNS records by zone_id",
      parameters: {
        type: "object",
        properties: {
          zone_id: { type: "number", description: "DNS zone ID" },
        },
        required: ["zone_id"],
      },
      run: async (params, context) => withClient(context, "isp_dns_record_list", (client) => client.call("dns_rr_get_all_by_zone", { zone_id: toNumber(params.zone_id ?? params.zoneId) })),
    },
    {
      name: "isp_dns_record_add",
      description: "Add DNS record using type-specific method",
      parameters: {
        type: "object",
        properties: {
          type: { type: "string", enum: DNS_RECORD_TYPES, description: "DNS record type" },
          client_id: { type: "number", description: "Client ID" },
          params: { type: "object", description: "DNS record parameters" },
        },
        required: ["type"],
      },
      run: async (params, context) => withClient(context, "isp_dns_record_add", (client) => {
        const method = dnsMethodForType(String(params.type ?? ""), "add");
        return client.call(method, params);
      }),
    },
    {
      name: "isp_dns_record_delete",
      description: "Delete DNS record using type-specific method",
      parameters: {
        type: "object",
        properties: {
          type: { type: "string", enum: DNS_RECORD_TYPES, description: "DNS record type" },
          primary_id: { type: "number", description: "DNS record primary ID to delete" },
          client_id: { type: "number", description: "Client ID" },
        },
        required: ["type"],
      },
      run: async (params, context) => withClient(context, "isp_dns_record_delete", (client) => {
        const method = dnsMethodForType(String(params.type ?? ""), "delete");
        return client.call(method, params);
      }),
    },
    {
      name: "isp_mail_domain_list",
      description: "List mail domains",
      parameters: { type: "object", properties: {} },
      run: async (params, context) => withClient(context, "isp_mail_domain_list", (client) => client.call("mail_domain_get", params)),
    },
    {
      name: "isp_mail_domain_add",
      description: "Create mail domain",
      parameters: {
        type: "object",
        properties: {
          client_id: { type: "number", description: "Client ID" },
          params: { type: "object", description: "Mail domain parameters" },
        },
        required: ["client_id", "params"],
      },
      run: async (params, context) => withClient(context, "isp_mail_domain_add", (client) => client.call("mail_domain_add", params)),
    },
    {
      name: "isp_mail_user_list",
      description: "List mail users",
      parameters: { type: "object", properties: {} },
      run: async (params, context) => withClient(context, "isp_mail_user_list", (client) => client.call("mail_user_get", params)),
    },
    {
      name: "isp_mail_user_add",
      description: "Create mail user",
      parameters: {
        type: "object",
        properties: {
          client_id: { type: "number", description: "Client ID" },
          params: { type: "object", description: "Mail user parameters" },
        },
        required: ["client_id", "params"],
      },
      run: async (params, context) => withClient(context, "isp_mail_user_add", (client) => client.call("mail_user_add", params)),
    },
    {
      name: "isp_mail_user_delete",
      description: "Delete mail user",
      parameters: {
        type: "object",
        properties: {
          primary_id: { type: "number", description: "Mail user ID to delete" },
        },
        required: ["primary_id"],
      },
      run: async (params, context) => withClient(context, "isp_mail_user_delete", (client) => client.call("mail_user_delete", params)),
    },
    {
      name: "isp_db_list",
      description: "List databases by user",
      parameters: { type: "object", properties: {} },
      run: async (params, context) => withClient(context, "isp_db_list", (client) => client.call("sites_database_get_all_by_user", params)),
    },
    {
      name: "isp_db_add",
      description: "Create database",
      parameters: {
        type: "object",
        properties: {
          client_id: { type: "number", description: "Client ID" },
          params: { type: "object", description: "Database parameters" },
        },
        required: ["client_id", "params"],
      },
      run: async (params, context) => withClient(context, "isp_db_add", (client) => client.call("sites_database_add", params)),
    },
    {
      name: "isp_db_user_add",
      description: "Create database user",
      parameters: {
        type: "object",
        properties: {
          client_id: { type: "number", description: "Client ID" },
          params: { type: "object", description: "Database user parameters" },
        },
        required: ["client_id", "params"],
      },
      run: async (params, context) => withClient(context, "isp_db_user_add", (client) => client.call("sites_database_user_add", params)),
    },
    {
      name: "isp_ssl_status",
      description: "Check SSL and Let's Encrypt status for sites",
      parameters: { type: "object", properties: {} },
      run: async (_params, context) => withClient(context, "isp_ssl_status", async (client) => {
        const sites = await fetchSites(client);
        const status = (sites ?? []).map((site) => ({
          domain: site.domain,
          ssl: site.ssl,
          ssl_letsencrypt: site.ssl_letsencrypt,
          active: site.active,
        }));
        return { total: status.length, status };
      }),
    },
    {
      name: "isp_quota_check",
      description: "Check quota values for a client",
      parameters: {
        type: "object",
        properties: {
          client_id: { type: "number", description: "Client ID" },
        },
        required: ["client_id"],
      },
      run: async (params, context) => withClient(context, "isp_quota_check", async (client) => {
        const details = await client.call<JsonMap>("client_get", { client_id: toNumber(params.client_id ?? params.clientId) });
        return {
          client_id: details.client_id,
          company_name: details.company_name,
          web_quota: details.web_quota,
          traffic_quota: details.traffic_quota,
        };
      }),
    },
    {
      name: "isp_backup_list",
      description: "Backup list if API supports backup methods",
      parameters: { type: "object", properties: {} },
      run: async (_params, context) => withClient(context, "isp_backup_list", async () => ({
        skipped: true,
        reason: "No backup list method discovered in ISPConfig API",
      })),
    },
    {
      name: "isp_shell_user_add",
      description: "Create shell user",
      parameters: {
        type: "object",
        properties: {
          client_id: { type: "number", description: "Client ID" },
          params: { type: "object", description: "Shell user parameters" },
        },
        required: ["client_id", "params"],
      },
      run: async (params, context) => withClient(context, "isp_shell_user_add", (client) => client.call("sites_shell_user_add", params)),
    },
    {
      name: "isp_ftp_user_add",
      description: "Create FTP user",
      parameters: {
        type: "object",
        properties: {
          client_id: { type: "number", description: "Client ID" },
          params: { type: "object", description: "FTP user parameters" },
        },
        required: ["client_id", "params"],
      },
      run: async (params, context) => withClient(context, "isp_ftp_user_add", (client) => client.call("sites_ftp_user_add", params)),
    },
    {
      name: "isp_cron_list",
      description: "List cron jobs",
      parameters: { type: "object", properties: {} },
      run: async (params, context) => withClient(context, "isp_cron_list", (client) => client.call("sites_cron_get", params)),
    },
    {
      name: "isp_cron_add",
      description: "Create cron job",
      parameters: {
        type: "object",
        properties: {
          client_id: { type: "number", description: "Client ID" },
          params: { type: "object", description: "Cron job parameters" },
        },
        required: ["client_id", "params"],
      },
      run: async (params, context) => withClient(context, "isp_cron_add", (client) => client.call("sites_cron_add", params)),
    },

    // -------------------------------------------------------------------------
    // New in v0.3.0 - Client management
    // -------------------------------------------------------------------------
    {
      name: "isp_client_update",
      description: "Update an existing ISPConfig client",
      parameters: {
        type: "object" as const,
        properties: {
          client_id: { type: "number", description: "Client ID" },
          params: { type: "object", description: "Fields to update" },
        },
        required: ["client_id", "params"],
      },
      run: async (params, context) => withClient(context, "isp_client_update", (client) =>
        client.call("client_update", params)),
    },
    {
      name: "isp_client_delete",
      description: "Delete an ISPConfig client",
      parameters: {
        type: "object" as const,
        properties: {
          client_id: { type: "number", description: "Client ID to delete" },
        },
        required: ["client_id"],
      },
      run: async (params, context) => withClient(context, "isp_client_delete", (client) =>
        client.call("client_delete", params)),
    },

    // -------------------------------------------------------------------------
    // New in v0.3.0 - Website/Domain management
    // -------------------------------------------------------------------------
    {
      name: "isp_site_update",
      description: "Update web site configuration",
      parameters: {
        type: "object" as const,
        properties: {
          client_id: { type: "number", description: "Client ID" },
          primary_id: { type: "number", description: "Site ID to update" },
          params: { type: "object", description: "Fields to update" },
        },
        required: ["client_id", "primary_id", "params"],
      },
      run: async (params, context) => withClient(context, "isp_site_update", (client) =>
        client.call("sites_web_domain_update", params)),
    },
    {
      name: "isp_site_delete",
      description: "Delete a web site",
      parameters: {
        type: "object" as const,
        properties: {
          primary_id: { type: "number", description: "Site ID to delete" },
        },
        required: ["primary_id"],
      },
      run: async (params, context) => withClient(context, "isp_site_delete", (client) =>
        client.call("sites_web_domain_delete", params)),
    },

    // -------------------------------------------------------------------------
    // New in v0.3.0 - Mail
    // -------------------------------------------------------------------------
    {
      name: "isp_mail_domain_delete",
      description: "Delete a mail domain",
      parameters: {
        type: "object" as const,
        properties: {
          primary_id: { type: "number", description: "Mail domain ID to delete" },
        },
        required: ["primary_id"],
      },
      run: async (params, context) => withClient(context, "isp_mail_domain_delete", (client) =>
        client.call("mail_domain_delete", params)),
    },
    {
      name: "isp_mail_alias_list",
      description: "List mail aliases",
      parameters: { type: "object" as const, properties: {} },
      run: async (params, context) => withClient(context, "isp_mail_alias_list", (client) =>
        client.call("mail_alias_get", params)),
    },
    {
      name: "isp_mail_alias_add",
      description: "Create a mail alias",
      parameters: {
        type: "object" as const,
        properties: {
          client_id: { type: "number", description: "Client ID" },
          params: { type: "object", description: "Mail alias parameters" },
        },
        required: ["client_id", "params"],
      },
      run: async (params, context) => withClient(context, "isp_mail_alias_add", (client) =>
        client.call("mail_alias_add", params)),
    },
    {
      name: "isp_mail_alias_delete",
      description: "Delete a mail alias",
      parameters: {
        type: "object" as const,
        properties: {
          primary_id: { type: "number", description: "Mail alias ID to delete" },
        },
        required: ["primary_id"],
      },
      run: async (params, context) => withClient(context, "isp_mail_alias_delete", (client) =>
        client.call("mail_alias_delete", params)),
    },
    {
      name: "isp_mail_forward_list",
      description: "List mail forwards",
      parameters: { type: "object" as const, properties: {} },
      run: async (params, context) => withClient(context, "isp_mail_forward_list", (client) =>
        client.call("mail_forward_get", params)),
    },
    {
      name: "isp_mail_forward_add",
      description: "Create a mail forward",
      parameters: {
        type: "object" as const,
        properties: {
          client_id: { type: "number", description: "Client ID" },
          params: { type: "object", description: "Mail forward parameters" },
        },
        required: ["client_id", "params"],
      },
      run: async (params, context) => withClient(context, "isp_mail_forward_add", (client) =>
        client.call("mail_forward_add", params)),
    },
    {
      name: "isp_mail_forward_delete",
      description: "Delete a mail forward",
      parameters: {
        type: "object" as const,
        properties: {
          primary_id: { type: "number", description: "Mail forward ID to delete" },
        },
        required: ["primary_id"],
      },
      run: async (params, context) => withClient(context, "isp_mail_forward_delete", (client) =>
        client.call("mail_forward_delete", params)),
    },

    // -------------------------------------------------------------------------
    // New in v0.3.0 - DNS
    // -------------------------------------------------------------------------
    {
      name: "isp_dns_zone_delete",
      description: "Delete a DNS zone",
      parameters: {
        type: "object" as const,
        properties: {
          primary_id: { type: "number", description: "DNS zone ID to delete" },
        },
        required: ["primary_id"],
      },
      run: async (params, context) => withClient(context, "isp_dns_zone_delete", (client) =>
        client.call("dns_zone_delete", params)),
    },
    {
      name: "isp_dns_record_update",
      description: "Update a DNS record using type-specific method",
      parameters: {
        type: "object" as const,
        properties: {
          type: { type: "string", enum: DNS_RECORD_TYPES, description: "DNS record type" },
          client_id: { type: "number", description: "Client ID" },
          primary_id: { type: "number", description: "DNS record ID to update" },
          params: { type: "object", description: "Fields to update" },
        },
        required: ["type", "primary_id"],
      },
      run: async (params, context) => withClient(context, "isp_dns_record_update", (client) => {
        const method = dnsMethodForType(String(params.type ?? ""), "update");
        return client.call(method, params);
      }),
    },

    // -------------------------------------------------------------------------
    // New in v0.3.0 - Databases
    // -------------------------------------------------------------------------
    {
      name: "isp_db_delete",
      description: "Delete a database",
      parameters: {
        type: "object" as const,
        properties: {
          primary_id: { type: "number", description: "Database ID to delete" },
        },
        required: ["primary_id"],
      },
      run: async (params, context) => withClient(context, "isp_db_delete", (client) =>
        client.call("sites_database_delete", params)),
    },
    {
      name: "isp_db_user_delete",
      description: "Delete a database user",
      parameters: {
        type: "object" as const,
        properties: {
          primary_id: { type: "number", description: "Database user ID to delete" },
        },
        required: ["primary_id"],
      },
      run: async (params, context) => withClient(context, "isp_db_user_delete", (client) =>
        client.call("sites_database_user_delete", params)),
    },

    // -------------------------------------------------------------------------
    // New in v0.3.0 - FTP / Shell
    // -------------------------------------------------------------------------
    {
      name: "isp_ftp_user_delete",
      description: "Delete an FTP user",
      parameters: {
        type: "object" as const,
        properties: {
          primary_id: { type: "number", description: "FTP user ID to delete" },
        },
        required: ["primary_id"],
      },
      run: async (params, context) => withClient(context, "isp_ftp_user_delete", (client) =>
        client.call("sites_ftp_user_delete", params)),
    },
    {
      name: "isp_shell_user_delete",
      description: "Delete a shell user",
      parameters: {
        type: "object" as const,
        properties: {
          primary_id: { type: "number", description: "Shell user ID to delete" },
        },
        required: ["primary_id"],
      },
      run: async (params, context) => withClient(context, "isp_shell_user_delete", (client) =>
        client.call("sites_shell_user_delete", params)),
    },

    // -------------------------------------------------------------------------
    // New in v0.3.0 - Cron
    // -------------------------------------------------------------------------
    {
      name: "isp_cron_delete",
      description: "Delete a cron job",
      parameters: {
        type: "object" as const,
        properties: {
          primary_id: { type: "number", description: "Cron job ID to delete" },
        },
        required: ["primary_id"],
      },
      run: async (params, context) => withClient(context, "isp_cron_delete", (client) =>
        client.call("sites_cron_delete", params)),
    },
    {
      name: "isp_cron_update",
      description: "Update an existing cron job",
      parameters: {
        type: "object" as const,
        properties: {
          client_id: { type: "number", description: "Client ID" },
          primary_id: { type: "number", description: "Cron job ID to update" },
          params: { type: "object", description: "Fields to update" },
        },
        required: ["client_id", "primary_id", "params"],
      },
      run: async (params, context) => withClient(context, "isp_cron_update", (client) =>
        client.call("sites_cron_update", params)),
    },

    // -------------------------------------------------------------------------
    // New in v0.4.0 - DNS zone get/update
    // -------------------------------------------------------------------------
    {
      name: "isp_dns_zone_get",
      description: "Get a single DNS zone by ID",
      parameters: {
        type: "object" as const,
        properties: {
          primary_id: { type: "number", description: "DNS zone ID" },
          zone_id: { type: "number", description: "Alias for primary_id" },
        },
      },
      run: async (params, context) => withClient(context, "isp_dns_zone_get", (client) =>
        client.call("dns_zone_get", { primary_id: toNumber(params.primary_id ?? params.zone_id) })),
    },
    {
      name: "isp_dns_zone_update",
      description: "Update DNS zone settings (SOA NS, TTL, refresh, etc.)",
      parameters: {
        type: "object" as const,
        properties: {
          client_id: { type: "number", description: "Client ID" },
          primary_id: { type: "number", description: "DNS zone ID to update" },
          params: { type: "object", description: "Fields to update (ns, mbox, refresh, retry, expire, minimum, ttl, active)" },
        },
        required: ["client_id", "primary_id", "params"],
      },
      run: async (params, context) => withClient(context, "isp_dns_zone_update", (client) =>
        client.call("dns_zone_update", params)),
    },

    // -------------------------------------------------------------------------
    // New in v0.4.0 - Mail updates
    // -------------------------------------------------------------------------
    {
      name: "isp_mail_domain_update",
      description: "Update mail domain settings",
      parameters: {
        type: "object" as const,
        properties: {
          client_id: { type: "number", description: "Client ID" },
          primary_id: { type: "number", description: "Mail domain ID to update" },
          params: { type: "object", description: "Fields to update" },
        },
        required: ["client_id", "primary_id", "params"],
      },
      run: async (params, context) => withClient(context, "isp_mail_domain_update", (client) =>
        client.call("mail_domain_update", params)),
    },
    {
      name: "isp_mail_user_update",
      description: "Update mail user (password, quota, etc.)",
      parameters: {
        type: "object" as const,
        properties: {
          client_id: { type: "number", description: "Client ID" },
          primary_id: { type: "number", description: "Mail user ID to update" },
          params: { type: "object", description: "Fields to update" },
        },
        required: ["client_id", "primary_id", "params"],
      },
      run: async (params, context) => withClient(context, "isp_mail_user_update", (client) =>
        client.call("mail_user_update", params)),
    },
    {
      name: "isp_mail_alias_update",
      description: "Update a mail alias",
      parameters: {
        type: "object" as const,
        properties: {
          client_id: { type: "number", description: "Client ID" },
          primary_id: { type: "number", description: "Mail alias ID to update" },
          params: { type: "object", description: "Fields to update" },
        },
        required: ["client_id", "primary_id", "params"],
      },
      run: async (params, context) => withClient(context, "isp_mail_alias_update", (client) =>
        client.call("mail_alias_update", params)),
    },
    {
      name: "isp_mail_forward_update",
      description: "Update a mail forward",
      parameters: {
        type: "object" as const,
        properties: {
          client_id: { type: "number", description: "Client ID" },
          primary_id: { type: "number", description: "Mail forward ID to update" },
          params: { type: "object", description: "Fields to update" },
        },
        required: ["client_id", "primary_id", "params"],
      },
      run: async (params, context) => withClient(context, "isp_mail_forward_update", (client) =>
        client.call("mail_forward_update", params)),
    },

    // -------------------------------------------------------------------------
    // New in v0.4.0 - Database get/update
    // -------------------------------------------------------------------------
    {
      name: "isp_db_get",
      description: "Get a single database by ID",
      parameters: {
        type: "object" as const,
        properties: {
          primary_id: { type: "number", description: "Database ID" },
        },
        required: ["primary_id"],
      },
      run: async (params, context) => withClient(context, "isp_db_get", (client) =>
        client.call("sites_database_get", { primary_id: toNumber(params.primary_id) })),
    },
    {
      name: "isp_db_update",
      description: "Update database settings",
      parameters: {
        type: "object" as const,
        properties: {
          client_id: { type: "number", description: "Client ID" },
          primary_id: { type: "number", description: "Database ID to update" },
          params: { type: "object", description: "Fields to update" },
        },
        required: ["client_id", "primary_id", "params"],
      },
      run: async (params, context) => withClient(context, "isp_db_update", (client) =>
        client.call("sites_database_update", params)),
    },
    {
      name: "isp_db_user_get",
      description: "Get a database user by ID",
      parameters: {
        type: "object" as const,
        properties: {
          primary_id: { type: "number", description: "Database user ID" },
        },
        required: ["primary_id"],
      },
      run: async (params, context) => withClient(context, "isp_db_user_get", (client) =>
        client.call("sites_database_user_get", { primary_id: toNumber(params.primary_id) })),
    },
    {
      name: "isp_db_user_update",
      description: "Update a database user",
      parameters: {
        type: "object" as const,
        properties: {
          client_id: { type: "number", description: "Client ID" },
          primary_id: { type: "number", description: "Database user ID to update" },
          params: { type: "object", description: "Fields to update" },
        },
        required: ["client_id", "primary_id", "params"],
      },
      run: async (params, context) => withClient(context, "isp_db_user_update", (client) =>
        client.call("sites_database_user_update", params)),
    },

    // -------------------------------------------------------------------------
    // New in v0.4.0 - FTP/Shell get/update
    // -------------------------------------------------------------------------
    {
      name: "isp_ftp_user_get",
      description: "Get FTP user details by ID",
      parameters: {
        type: "object" as const,
        properties: {
          primary_id: { type: "number", description: "FTP user ID" },
        },
        required: ["primary_id"],
      },
      run: async (params, context) => withClient(context, "isp_ftp_user_get", (client) =>
        client.call("sites_ftp_user_get", { primary_id: toNumber(params.primary_id) })),
    },
    {
      name: "isp_ftp_user_update",
      description: "Update an FTP user",
      parameters: {
        type: "object" as const,
        properties: {
          client_id: { type: "number", description: "Client ID" },
          primary_id: { type: "number", description: "FTP user ID to update" },
          params: { type: "object", description: "Fields to update" },
        },
        required: ["client_id", "primary_id", "params"],
      },
      run: async (params, context) => withClient(context, "isp_ftp_user_update", (client) =>
        client.call("sites_ftp_user_update", params)),
    },
    {
      name: "isp_shell_user_get",
      description: "Get shell user details by ID",
      parameters: {
        type: "object" as const,
        properties: {
          primary_id: { type: "number", description: "Shell user ID" },
        },
        required: ["primary_id"],
      },
      run: async (params, context) => withClient(context, "isp_shell_user_get", (client) =>
        client.call("sites_shell_user_get", { primary_id: toNumber(params.primary_id) })),
    },
    {
      name: "isp_shell_user_update",
      description: "Update a shell user",
      parameters: {
        type: "object" as const,
        properties: {
          client_id: { type: "number", description: "Client ID" },
          primary_id: { type: "number", description: "Shell user ID to update" },
          params: { type: "object", description: "Fields to update" },
        },
        required: ["client_id", "primary_id", "params"],
      },
      run: async (params, context) => withClient(context, "isp_shell_user_update", (client) =>
        client.call("sites_shell_user_update", params)),
    },

    // -------------------------------------------------------------------------
    // New in v0.5.0 — Phase 1: Core Completion (32 tools)
    // -------------------------------------------------------------------------

    // --- Clients (14 new) ---
    {
      name: "isp_client_get_id",
      description: "Get client ID by system user ID",
      parameters: {
        type: "object" as const,
        properties: {
          sys_userid: { type: "number", description: "System user ID" },
        },
        required: ["sys_userid"],
      },
      run: async (params, context) => withClient(context, "isp_client_get_id", (client) =>
        client.call("client_get_id", { sys_userid: toNumber(params.sys_userid) })),
    },
    {
      name: "isp_client_get_email",
      description: "Get client email contact information",
      parameters: {
        type: "object" as const,
        properties: {
          client_id: { type: "number", description: "Client ID" },
        },
        required: ["client_id"],
      },
      run: async (params, context) => withClient(context, "isp_client_get_email", (client) =>
        client.call("client_get_emailcontact", { client_id: toNumber(params.client_id) })),
    },
    {
      name: "isp_client_get_groupid",
      description: "Get client group ID",
      parameters: {
        type: "object" as const,
        properties: {
          client_id: { type: "number", description: "Client ID" },
        },
        required: ["client_id"],
      },
      run: async (params, context) => withClient(context, "isp_client_get_groupid", (client) =>
        client.call("client_get_groupid", { client_id: toNumber(params.client_id) })),
    },
    {
      name: "isp_client_get_by_username",
      description: "Look up client by username",
      parameters: {
        type: "object" as const,
        properties: {
          username: { type: "string", description: "Client username" },
        },
        required: ["username"],
      },
      run: async (params, context) => withClient(context, "isp_client_get_by_username", (client) =>
        client.call("client_get_by_username", { username: String(params.username) })),
    },
    {
      name: "isp_client_get_by_customer_no",
      description: "Look up client by customer number",
      parameters: {
        type: "object" as const,
        properties: {
          customer_no: { type: "string", description: "Customer number" },
        },
        required: ["customer_no"],
      },
      run: async (params, context) => withClient(context, "isp_client_get_by_customer_no", (client) =>
        client.call("client_get_by_customer_no", { customer_no: String(params.customer_no) })),
    },
    {
      name: "isp_client_get_by_groupid",
      description: "Look up client by group ID",
      parameters: {
        type: "object" as const,
        properties: {
          groupid: { type: "number", description: "Group ID" },
        },
        required: ["groupid"],
      },
      run: async (params, context) => withClient(context, "isp_client_get_by_groupid", (client) =>
        client.call("client_get_by_groupid", { groupid: toNumber(params.groupid) })),
    },
    {
      name: "isp_client_get_sites",
      description: "List sites for a client user",
      parameters: {
        type: "object" as const,
        properties: {
          sys_userid: { type: "number", description: "System user ID" },
          sys_groupid: { type: "number", description: "System group ID" },
        },
        required: ["sys_userid", "sys_groupid"],
      },
      run: async (params, context) => withClient(context, "isp_client_get_sites", (client) =>
        client.call("client_get_sites_by_user", { sys_userid: toNumber(params.sys_userid), sys_groupid: toNumber(params.sys_groupid) })),
    },
    {
      name: "isp_client_change_password",
      description: "Change client password",
      parameters: {
        type: "object" as const,
        properties: {
          client_id: { type: "number", description: "Client ID" },
          password: { type: "string", description: "New password" },
        },
        required: ["client_id", "password"],
      },
      run: async (params, context) => withClient(context, "isp_client_change_password", (client) =>
        client.call("client_change_password", { client_id: toNumber(params.client_id), password: String(params.password) })),
    },
    {
      name: "isp_client_delete_everything",
      description: "Delete client and all associated data (sites, DNS, mail, databases)",
      parameters: {
        type: "object" as const,
        properties: {
          client_id: { type: "number", description: "Client ID to delete" },
        },
        required: ["client_id"],
      },
      run: async (params, context) => withClient(context, "isp_client_delete_everything", (client) =>
        client.call("client_delete_everything", { client_id: toNumber(params.client_id) })),
    },
    {
      name: "isp_client_login_get",
      description: "Get client login data",
      parameters: {
        type: "object" as const,
        properties: {
          client_id: { type: "number", description: "Client ID" },
        },
        required: ["client_id"],
      },
      run: async (params, context) => withClient(context, "isp_client_login_get", (client) =>
        client.call("client_login_get", { client_id: toNumber(params.client_id) })),
    },
    {
      name: "isp_client_template_get",
      description: "Get additional client template assignment",
      parameters: {
        type: "object" as const,
        properties: {
          client_id: { type: "number", description: "Client ID" },
          template_id: { type: "number", description: "Template ID" },
        },
        required: ["client_id", "template_id"],
      },
      run: async (params, context) => withClient(context, "isp_client_template_get", (client) =>
        client.call("client_template_additional_get", { client_id: toNumber(params.client_id), template_id: toNumber(params.template_id) })),
    },
    {
      name: "isp_client_template_add",
      description: "Add additional template to client",
      parameters: {
        type: "object" as const,
        properties: {
          client_id: { type: "number", description: "Client ID" },
          template_id: { type: "number", description: "Template ID to assign" },
        },
        required: ["client_id", "template_id"],
      },
      run: async (params, context) => withClient(context, "isp_client_template_add", (client) =>
        client.call("client_template_additional_add", { client_id: toNumber(params.client_id), template_id: toNumber(params.template_id) })),
    },
    {
      name: "isp_client_template_delete",
      description: "Delete additional template from client",
      parameters: {
        type: "object" as const,
        properties: {
          assigned_template_id: { type: "number", description: "Assigned template ID to remove" },
        },
        required: ["assigned_template_id"],
      },
      run: async (params, context) => withClient(context, "isp_client_template_delete", (client) =>
        client.call("client_template_additional_delete", { assigned_template_id: toNumber(params.assigned_template_id) })),
    },
    {
      name: "isp_client_templates_list",
      description: "List all available client templates",
      parameters: { type: "object" as const, properties: {} },
      run: async (_params, context) => withClient(context, "isp_client_templates_list", (client) =>
        client.call("client_templates_get_all", {})),
    },

    // --- Server (10 new) ---
    {
      name: "isp_server_get_version",
      description: "Get ISPConfig application version",
      parameters: { type: "object" as const, properties: {} },
      run: async (_params, context) => withClient(context, "isp_server_get_version", (client) =>
        client.call("server_get_app_version", {})),
    },
    {
      name: "isp_server_get_functions",
      description: "Get available functions for a server",
      parameters: {
        type: "object" as const,
        properties: {
          server_id: { type: "number", description: "Server ID" },
        },
        required: ["server_id"],
      },
      run: async (params, context) => withClient(context, "isp_server_get_functions", (client) =>
        client.call("server_get_functions", { server_id: toNumber(params.server_id) })),
    },
    {
      name: "isp_server_get_php_versions",
      description: "List available PHP versions on a server",
      parameters: {
        type: "object" as const,
        properties: {
          server_id: { type: "number", description: "Server ID" },
          type: { type: "string", description: "PHP handler type (e.g. php-fpm, fast-cgi)" },
        },
        required: ["server_id"],
      },
      run: async (params, context) => withClient(context, "isp_server_get_php_versions", (client) =>
        client.call("server_get_php_versions", { server_id: toNumber(params.server_id), ...(params.type ? { type: String(params.type) } : {}) })),
    },
    {
      name: "isp_server_get_by_ip",
      description: "Look up server ID by IP address",
      parameters: {
        type: "object" as const,
        properties: {
          ipaddress: { type: "string", description: "IP address" },
        },
        required: ["ipaddress"],
      },
      run: async (params, context) => withClient(context, "isp_server_get_by_ip", (client) =>
        client.call("server_get_serverid_by_ip", { ipaddress: String(params.ipaddress) })),
    },
    {
      name: "isp_server_get_by_name",
      description: "Look up server ID by server name",
      parameters: {
        type: "object" as const,
        properties: {
          server_name: { type: "string", description: "Server name" },
        },
        required: ["server_name"],
      },
      run: async (params, context) => withClient(context, "isp_server_get_by_name", (client) =>
        client.call("server_get_serverid_by_name", { server_name: String(params.server_name) })),
    },
    {
      name: "isp_server_ip_get",
      description: "Get server IP details",
      parameters: {
        type: "object" as const,
        properties: {
          primary_id: { type: "number", description: "Server IP record ID" },
        },
        required: ["primary_id"],
      },
      run: async (params, context) => withClient(context, "isp_server_ip_get", (client) =>
        client.call("server_ip_get", { primary_id: toNumber(params.primary_id) })),
    },
    {
      name: "isp_server_ip_add",
      description: "Add a server IP address",
      parameters: {
        type: "object" as const,
        properties: {
          client_id: { type: "number", description: "Client ID" },
          params: { type: "object", description: "Server IP parameters (server_id, ip_address, etc.)" },
        },
        required: ["client_id", "params"],
      },
      run: async (params, context) => withClient(context, "isp_server_ip_add", (client) =>
        client.call("server_ip_add", params)),
    },
    {
      name: "isp_server_ip_update",
      description: "Update a server IP address",
      parameters: {
        type: "object" as const,
        properties: {
          client_id: { type: "number", description: "Client ID" },
          primary_id: { type: "number", description: "Server IP record ID" },
          params: { type: "object", description: "Fields to update" },
        },
        required: ["client_id", "primary_id", "params"],
      },
      run: async (params, context) => withClient(context, "isp_server_ip_update", (client) =>
        client.call("server_ip_update", params)),
    },
    {
      name: "isp_server_ip_delete",
      description: "Delete a server IP address",
      parameters: {
        type: "object" as const,
        properties: {
          primary_id: { type: "number", description: "Server IP record ID to delete" },
        },
        required: ["primary_id"],
      },
      run: async (params, context) => withClient(context, "isp_server_ip_delete", (client) =>
        client.call("server_ip_delete", { primary_id: toNumber(params.primary_id) })),
    },
    {
      name: "isp_server_config_set",
      description: "Update server configuration",
      parameters: {
        type: "object" as const,
        properties: {
          server_id: { type: "number", description: "Server ID" },
          section: { type: "string", description: "Config section name" },
          params: { type: "object", description: "Configuration key-value pairs" },
        },
        required: ["server_id", "section", "params"],
      },
      run: async (params, context) => withClient(context, "isp_server_config_set", (client) =>
        client.call("server_config_set", params)),
    },

    // --- Web Domains (3 new) ---
    {
      name: "isp_site_backup",
      description: "Trigger a site backup",
      parameters: {
        type: "object" as const,
        properties: {
          primary_id: { type: "number", description: "Site ID to backup" },
          params: { type: "object", description: "Backup parameters (action_type, backup_mode)" },
        },
        required: ["primary_id"],
      },
      run: async (params, context) => withClient(context, "isp_site_backup", (client) =>
        client.call("sites_web_domain_backup", params)),
    },
    {
      name: "isp_site_backup_list",
      description: "List backups for a site",
      parameters: {
        type: "object" as const,
        properties: {
          primary_id: { type: "number", description: "Site ID" },
        },
        required: ["primary_id"],
      },
      run: async (params, context) => withClient(context, "isp_site_backup_list", (client) =>
        client.call("sites_web_domain_backup_list", { primary_id: toNumber(params.primary_id) })),
    },
    {
      name: "isp_site_set_status",
      description: "Enable or disable a web site",
      parameters: {
        type: "object" as const,
        properties: {
          primary_id: { type: "number", description: "Site ID" },
          status: { type: "string", enum: ["active", "inactive"], description: "New status" },
        },
        required: ["primary_id", "status"],
      },
      run: async (params, context) => withClient(context, "isp_site_set_status", (client) =>
        client.call("sites_web_domain_set_status", { primary_id: toNumber(params.primary_id), status: String(params.status) })),
    },

    // --- Quota & Traffic (4 new) ---
    {
      name: "isp_quota_get",
      description: "Get disk quota data for a user",
      parameters: {
        type: "object" as const,
        properties: {
          client_group_id: { type: "number", description: "Client group ID" },
        },
        required: ["client_group_id"],
      },
      run: async (params, context) => withClient(context, "isp_quota_get", (client) =>
        client.call("quota_get_by_user", { client_group_id: toNumber(params.client_group_id) })),
    },
    {
      name: "isp_traffic_get",
      description: "Get traffic quota data for a user",
      parameters: {
        type: "object" as const,
        properties: {
          client_group_id: { type: "number", description: "Client group ID" },
          lastdays: { type: "number", description: "Number of days to look back (default: current month)" },
        },
        required: ["client_group_id"],
      },
      run: async (params, context) => withClient(context, "isp_traffic_get", (client) =>
        client.call("trafficquota_get_by_user", { client_group_id: toNumber(params.client_group_id), ...(params.lastdays !== undefined ? { lastdays: toNumber(params.lastdays) } : {}) })),
    },
    {
      name: "isp_ftp_traffic_get",
      description: "Get FTP traffic data",
      parameters: {
        type: "object" as const,
        properties: {
          year: { type: "number", description: "Year" },
          month: { type: "number", description: "Month (1-12)" },
        },
        required: ["year", "month"],
      },
      run: async (params, context) => withClient(context, "isp_ftp_traffic_get", (client) =>
        client.call("ftptrafficquota_data", { year: toNumber(params.year), month: toNumber(params.month) })),
    },
    {
      name: "isp_db_quota_get",
      description: "Get database quota data for a user",
      parameters: {
        type: "object" as const,
        properties: {
          client_group_id: { type: "number", description: "Client group ID" },
        },
        required: ["client_group_id"],
      },
      run: async (params, context) => withClient(context, "isp_db_quota_get", (client) =>
        client.call("databasequota_get_by_user", { client_group_id: toNumber(params.client_group_id) })),
    },

    // --- Monitoring (1 new) ---
    {
      name: "isp_monitor_jobqueue",
      description: "Get count of pending jobs in the ISPConfig job queue",
      parameters: { type: "object" as const, properties: {} },
      run: async (_params, context) => withClient(context, "isp_monitor_jobqueue", (client) =>
        client.call("monitor_jobqueue_count", {})),
    },

    // -------------------------------------------------------------------------
    // New in v0.6.0 — Phase 2: DNS Complete
    // -------------------------------------------------------------------------

    // --- DNS Record Gets (9 new) ---
    {
      name: "isp_dns_a_get",
      description: "Get a single DNS A record by ID",
      parameters: {
        type: "object" as const,
        properties: {
          primary_id: { type: "number", description: "DNS record ID" },
        },
        required: ["primary_id"],
      },
      run: async (params, context) => withClient(context, "isp_dns_a_get", (client) =>
        client.call("dns_a_get", { primary_id: toNumber(params.primary_id) })),
    },
    {
      name: "isp_dns_aaaa_get",
      description: "Get a single DNS AAAA record by ID",
      parameters: {
        type: "object" as const,
        properties: {
          primary_id: { type: "number", description: "DNS record ID" },
        },
        required: ["primary_id"],
      },
      run: async (params, context) => withClient(context, "isp_dns_aaaa_get", (client) =>
        client.call("dns_aaaa_get", { primary_id: toNumber(params.primary_id) })),
    },
    {
      name: "isp_dns_caa_get",
      description: "Get a single DNS CAA record by ID",
      parameters: {
        type: "object" as const,
        properties: {
          primary_id: { type: "number", description: "DNS record ID" },
        },
        required: ["primary_id"],
      },
      run: async (params, context) => withClient(context, "isp_dns_caa_get", (client) =>
        client.call("dns_caa_get", { primary_id: toNumber(params.primary_id) })),
    },
    {
      name: "isp_dns_cname_get",
      description: "Get a single DNS CNAME record by ID",
      parameters: {
        type: "object" as const,
        properties: {
          primary_id: { type: "number", description: "DNS record ID" },
        },
        required: ["primary_id"],
      },
      run: async (params, context) => withClient(context, "isp_dns_cname_get", (client) =>
        client.call("dns_cname_get", { primary_id: toNumber(params.primary_id) })),
    },
    {
      name: "isp_dns_mx_get",
      description: "Get a single DNS MX record by ID",
      parameters: {
        type: "object" as const,
        properties: {
          primary_id: { type: "number", description: "DNS record ID" },
        },
        required: ["primary_id"],
      },
      run: async (params, context) => withClient(context, "isp_dns_mx_get", (client) =>
        client.call("dns_mx_get", { primary_id: toNumber(params.primary_id) })),
    },
    {
      name: "isp_dns_ns_get",
      description: "Get a single DNS NS record by ID",
      parameters: {
        type: "object" as const,
        properties: {
          primary_id: { type: "number", description: "DNS record ID" },
        },
        required: ["primary_id"],
      },
      run: async (params, context) => withClient(context, "isp_dns_ns_get", (client) =>
        client.call("dns_ns_get", { primary_id: toNumber(params.primary_id) })),
    },
    {
      name: "isp_dns_ptr_get",
      description: "Get a single DNS PTR record by ID",
      parameters: {
        type: "object" as const,
        properties: {
          primary_id: { type: "number", description: "DNS record ID" },
        },
        required: ["primary_id"],
      },
      run: async (params, context) => withClient(context, "isp_dns_ptr_get", (client) =>
        client.call("dns_ptr_get", { primary_id: toNumber(params.primary_id) })),
    },
    {
      name: "isp_dns_srv_get",
      description: "Get a single DNS SRV record by ID",
      parameters: {
        type: "object" as const,
        properties: {
          primary_id: { type: "number", description: "DNS record ID" },
        },
        required: ["primary_id"],
      },
      run: async (params, context) => withClient(context, "isp_dns_srv_get", (client) =>
        client.call("dns_srv_get", { primary_id: toNumber(params.primary_id) })),
    },
    {
      name: "isp_dns_txt_get",
      description: "Get a single DNS TXT record by ID",
      parameters: {
        type: "object" as const,
        properties: {
          primary_id: { type: "number", description: "DNS record ID" },
        },
        required: ["primary_id"],
      },
      run: async (params, context) => withClient(context, "isp_dns_txt_get", (client) =>
        client.call("dns_txt_get", { primary_id: toNumber(params.primary_id) })),
    },

    // --- DNS ALIAS records (4 new) ---
    {
      name: "isp_dns_alias_get",
      description: "Get a single DNS ALIAS record by ID",
      parameters: {
        type: "object" as const,
        properties: {
          primary_id: { type: "number", description: "DNS record ID" },
        },
        required: ["primary_id"],
      },
      run: async (params, context) => withClient(context, "isp_dns_alias_get", (client) =>
        client.call("dns_alias_get", { primary_id: toNumber(params.primary_id) })),
    },
    {
      name: "isp_dns_alias_add",
      description: "Add a DNS ALIAS record",
      parameters: {
        type: "object" as const,
        properties: {
          client_id: { type: "number", description: "Client ID" },
          params: { type: "object", description: "DNS ALIAS record parameters" },
        },
        required: ["client_id", "params"],
      },
      run: async (params, context) => withClient(context, "isp_dns_alias_add", (client) =>
        client.call("dns_alias_add", params)),
    },
    {
      name: "isp_dns_alias_update",
      description: "Update a DNS ALIAS record",
      parameters: {
        type: "object" as const,
        properties: {
          client_id: { type: "number", description: "Client ID" },
          primary_id: { type: "number", description: "DNS record ID to update" },
          params: { type: "object", description: "Fields to update" },
        },
        required: ["client_id", "primary_id", "params"],
      },
      run: async (params, context) => withClient(context, "isp_dns_alias_update", (client) =>
        client.call("dns_alias_update", params)),
    },
    {
      name: "isp_dns_alias_delete",
      description: "Delete a DNS ALIAS record",
      parameters: {
        type: "object" as const,
        properties: {
          primary_id: { type: "number", description: "DNS record ID to delete" },
        },
        required: ["primary_id"],
      },
      run: async (params, context) => withClient(context, "isp_dns_alias_delete", (client) =>
        client.call("dns_alias_delete", { primary_id: toNumber(params.primary_id) })),
    },

    // --- DNS DNAME records (4 new) ---
    {
      name: "isp_dns_dname_get",
      description: "Get a single DNS DNAME record by ID",
      parameters: {
        type: "object" as const,
        properties: {
          primary_id: { type: "number", description: "DNS record ID" },
        },
        required: ["primary_id"],
      },
      run: async (params, context) => withClient(context, "isp_dns_dname_get", (client) =>
        client.call("dns_dname_get", { primary_id: toNumber(params.primary_id) })),
    },
    {
      name: "isp_dns_dname_add",
      description: "Add a DNS DNAME record",
      parameters: {
        type: "object" as const,
        properties: {
          client_id: { type: "number", description: "Client ID" },
          params: { type: "object", description: "DNS DNAME record parameters" },
        },
        required: ["client_id", "params"],
      },
      run: async (params, context) => withClient(context, "isp_dns_dname_add", (client) =>
        client.call("dns_dname_add", params)),
    },
    {
      name: "isp_dns_dname_update",
      description: "Update a DNS DNAME record",
      parameters: {
        type: "object" as const,
        properties: {
          client_id: { type: "number", description: "Client ID" },
          primary_id: { type: "number", description: "DNS record ID to update" },
          params: { type: "object", description: "Fields to update" },
        },
        required: ["client_id", "primary_id", "params"],
      },
      run: async (params, context) => withClient(context, "isp_dns_dname_update", (client) =>
        client.call("dns_dname_update", params)),
    },
    {
      name: "isp_dns_dname_delete",
      description: "Delete a DNS DNAME record",
      parameters: {
        type: "object" as const,
        properties: {
          primary_id: { type: "number", description: "DNS record ID to delete" },
        },
        required: ["primary_id"],
      },
      run: async (params, context) => withClient(context, "isp_dns_dname_delete", (client) =>
        client.call("dns_dname_delete", { primary_id: toNumber(params.primary_id) })),
    },

    // --- DNS DS records (4 new) ---
    {
      name: "isp_dns_ds_get",
      description: "Get a single DNS DS record by ID",
      parameters: {
        type: "object" as const,
        properties: {
          primary_id: { type: "number", description: "DNS record ID" },
        },
        required: ["primary_id"],
      },
      run: async (params, context) => withClient(context, "isp_dns_ds_get", (client) =>
        client.call("dns_ds_get", { primary_id: toNumber(params.primary_id) })),
    },
    {
      name: "isp_dns_ds_add",
      description: "Add a DNS DS record",
      parameters: {
        type: "object" as const,
        properties: {
          client_id: { type: "number", description: "Client ID" },
          params: { type: "object", description: "DNS DS record parameters" },
        },
        required: ["client_id", "params"],
      },
      run: async (params, context) => withClient(context, "isp_dns_ds_add", (client) =>
        client.call("dns_ds_add", params)),
    },
    {
      name: "isp_dns_ds_update",
      description: "Update a DNS DS record",
      parameters: {
        type: "object" as const,
        properties: {
          client_id: { type: "number", description: "Client ID" },
          primary_id: { type: "number", description: "DNS record ID to update" },
          params: { type: "object", description: "Fields to update" },
        },
        required: ["client_id", "primary_id", "params"],
      },
      run: async (params, context) => withClient(context, "isp_dns_ds_update", (client) =>
        client.call("dns_ds_update", params)),
    },
    {
      name: "isp_dns_ds_delete",
      description: "Delete a DNS DS record",
      parameters: {
        type: "object" as const,
        properties: {
          primary_id: { type: "number", description: "DNS record ID to delete" },
        },
        required: ["primary_id"],
      },
      run: async (params, context) => withClient(context, "isp_dns_ds_delete", (client) =>
        client.call("dns_ds_delete", { primary_id: toNumber(params.primary_id) })),
    },

    // --- DNS HINFO records (4 new) ---
    {
      name: "isp_dns_hinfo_get",
      description: "Get a single DNS HINFO record by ID",
      parameters: {
        type: "object" as const,
        properties: {
          primary_id: { type: "number", description: "DNS record ID" },
        },
        required: ["primary_id"],
      },
      run: async (params, context) => withClient(context, "isp_dns_hinfo_get", (client) =>
        client.call("dns_hinfo_get", { primary_id: toNumber(params.primary_id) })),
    },
    {
      name: "isp_dns_hinfo_add",
      description: "Add a DNS HINFO record",
      parameters: {
        type: "object" as const,
        properties: {
          client_id: { type: "number", description: "Client ID" },
          params: { type: "object", description: "DNS HINFO record parameters" },
        },
        required: ["client_id", "params"],
      },
      run: async (params, context) => withClient(context, "isp_dns_hinfo_add", (client) =>
        client.call("dns_hinfo_add", params)),
    },
    {
      name: "isp_dns_hinfo_update",
      description: "Update a DNS HINFO record",
      parameters: {
        type: "object" as const,
        properties: {
          client_id: { type: "number", description: "Client ID" },
          primary_id: { type: "number", description: "DNS record ID to update" },
          params: { type: "object", description: "Fields to update" },
        },
        required: ["client_id", "primary_id", "params"],
      },
      run: async (params, context) => withClient(context, "isp_dns_hinfo_update", (client) =>
        client.call("dns_hinfo_update", params)),
    },
    {
      name: "isp_dns_hinfo_delete",
      description: "Delete a DNS HINFO record",
      parameters: {
        type: "object" as const,
        properties: {
          primary_id: { type: "number", description: "DNS record ID to delete" },
        },
        required: ["primary_id"],
      },
      run: async (params, context) => withClient(context, "isp_dns_hinfo_delete", (client) =>
        client.call("dns_hinfo_delete", { primary_id: toNumber(params.primary_id) })),
    },

    // --- DNS LOC records (4 new) ---
    {
      name: "isp_dns_loc_get",
      description: "Get a single DNS LOC record by ID",
      parameters: {
        type: "object" as const,
        properties: {
          primary_id: { type: "number", description: "DNS record ID" },
        },
        required: ["primary_id"],
      },
      run: async (params, context) => withClient(context, "isp_dns_loc_get", (client) =>
        client.call("dns_loc_get", { primary_id: toNumber(params.primary_id) })),
    },
    {
      name: "isp_dns_loc_add",
      description: "Add a DNS LOC record",
      parameters: {
        type: "object" as const,
        properties: {
          client_id: { type: "number", description: "Client ID" },
          params: { type: "object", description: "DNS LOC record parameters" },
        },
        required: ["client_id", "params"],
      },
      run: async (params, context) => withClient(context, "isp_dns_loc_add", (client) =>
        client.call("dns_loc_add", params)),
    },
    {
      name: "isp_dns_loc_update",
      description: "Update a DNS LOC record",
      parameters: {
        type: "object" as const,
        properties: {
          client_id: { type: "number", description: "Client ID" },
          primary_id: { type: "number", description: "DNS record ID to update" },
          params: { type: "object", description: "Fields to update" },
        },
        required: ["client_id", "primary_id", "params"],
      },
      run: async (params, context) => withClient(context, "isp_dns_loc_update", (client) =>
        client.call("dns_loc_update", params)),
    },
    {
      name: "isp_dns_loc_delete",
      description: "Delete a DNS LOC record",
      parameters: {
        type: "object" as const,
        properties: {
          primary_id: { type: "number", description: "DNS record ID to delete" },
        },
        required: ["primary_id"],
      },
      run: async (params, context) => withClient(context, "isp_dns_loc_delete", (client) =>
        client.call("dns_loc_delete", { primary_id: toNumber(params.primary_id) })),
    },

    // --- DNS NAPTR records (4 new) ---
    {
      name: "isp_dns_naptr_get",
      description: "Get a single DNS NAPTR record by ID",
      parameters: {
        type: "object" as const,
        properties: {
          primary_id: { type: "number", description: "DNS record ID" },
        },
        required: ["primary_id"],
      },
      run: async (params, context) => withClient(context, "isp_dns_naptr_get", (client) =>
        client.call("dns_naptr_get", { primary_id: toNumber(params.primary_id) })),
    },
    {
      name: "isp_dns_naptr_add",
      description: "Add a DNS NAPTR record",
      parameters: {
        type: "object" as const,
        properties: {
          client_id: { type: "number", description: "Client ID" },
          params: { type: "object", description: "DNS NAPTR record parameters" },
        },
        required: ["client_id", "params"],
      },
      run: async (params, context) => withClient(context, "isp_dns_naptr_add", (client) =>
        client.call("dns_naptr_add", params)),
    },
    {
      name: "isp_dns_naptr_update",
      description: "Update a DNS NAPTR record",
      parameters: {
        type: "object" as const,
        properties: {
          client_id: { type: "number", description: "Client ID" },
          primary_id: { type: "number", description: "DNS record ID to update" },
          params: { type: "object", description: "Fields to update" },
        },
        required: ["client_id", "primary_id", "params"],
      },
      run: async (params, context) => withClient(context, "isp_dns_naptr_update", (client) =>
        client.call("dns_naptr_update", params)),
    },
    {
      name: "isp_dns_naptr_delete",
      description: "Delete a DNS NAPTR record",
      parameters: {
        type: "object" as const,
        properties: {
          primary_id: { type: "number", description: "DNS record ID to delete" },
        },
        required: ["primary_id"],
      },
      run: async (params, context) => withClient(context, "isp_dns_naptr_delete", (client) =>
        client.call("dns_naptr_delete", { primary_id: toNumber(params.primary_id) })),
    },

    // --- DNS RP records (4 new) ---
    {
      name: "isp_dns_rp_get",
      description: "Get a single DNS RP record by ID",
      parameters: {
        type: "object" as const,
        properties: {
          primary_id: { type: "number", description: "DNS record ID" },
        },
        required: ["primary_id"],
      },
      run: async (params, context) => withClient(context, "isp_dns_rp_get", (client) =>
        client.call("dns_rp_get", { primary_id: toNumber(params.primary_id) })),
    },
    {
      name: "isp_dns_rp_add",
      description: "Add a DNS RP record",
      parameters: {
        type: "object" as const,
        properties: {
          client_id: { type: "number", description: "Client ID" },
          params: { type: "object", description: "DNS RP record parameters" },
        },
        required: ["client_id", "params"],
      },
      run: async (params, context) => withClient(context, "isp_dns_rp_add", (client) =>
        client.call("dns_rp_add", params)),
    },
    {
      name: "isp_dns_rp_update",
      description: "Update a DNS RP record",
      parameters: {
        type: "object" as const,
        properties: {
          client_id: { type: "number", description: "Client ID" },
          primary_id: { type: "number", description: "DNS record ID to update" },
          params: { type: "object", description: "Fields to update" },
        },
        required: ["client_id", "primary_id", "params"],
      },
      run: async (params, context) => withClient(context, "isp_dns_rp_update", (client) =>
        client.call("dns_rp_update", params)),
    },
    {
      name: "isp_dns_rp_delete",
      description: "Delete a DNS RP record",
      parameters: {
        type: "object" as const,
        properties: {
          primary_id: { type: "number", description: "DNS record ID to delete" },
        },
        required: ["primary_id"],
      },
      run: async (params, context) => withClient(context, "isp_dns_rp_delete", (client) =>
        client.call("dns_rp_delete", { primary_id: toNumber(params.primary_id) })),
    },

    // --- DNS SSHFP records (4 new) ---
    {
      name: "isp_dns_sshfp_get",
      description: "Get a single DNS SSHFP record by ID",
      parameters: {
        type: "object" as const,
        properties: {
          primary_id: { type: "number", description: "DNS record ID" },
        },
        required: ["primary_id"],
      },
      run: async (params, context) => withClient(context, "isp_dns_sshfp_get", (client) =>
        client.call("dns_sshfp_get", { primary_id: toNumber(params.primary_id) })),
    },
    {
      name: "isp_dns_sshfp_add",
      description: "Add a DNS SSHFP record",
      parameters: {
        type: "object" as const,
        properties: {
          client_id: { type: "number", description: "Client ID" },
          params: { type: "object", description: "DNS SSHFP record parameters" },
        },
        required: ["client_id", "params"],
      },
      run: async (params, context) => withClient(context, "isp_dns_sshfp_add", (client) =>
        client.call("dns_sshfp_add", params)),
    },
    {
      name: "isp_dns_sshfp_update",
      description: "Update a DNS SSHFP record",
      parameters: {
        type: "object" as const,
        properties: {
          client_id: { type: "number", description: "Client ID" },
          primary_id: { type: "number", description: "DNS record ID to update" },
          params: { type: "object", description: "Fields to update" },
        },
        required: ["client_id", "primary_id", "params"],
      },
      run: async (params, context) => withClient(context, "isp_dns_sshfp_update", (client) =>
        client.call("dns_sshfp_update", params)),
    },
    {
      name: "isp_dns_sshfp_delete",
      description: "Delete a DNS SSHFP record",
      parameters: {
        type: "object" as const,
        properties: {
          primary_id: { type: "number", description: "DNS record ID to delete" },
        },
        required: ["primary_id"],
      },
      run: async (params, context) => withClient(context, "isp_dns_sshfp_delete", (client) =>
        client.call("dns_sshfp_delete", { primary_id: toNumber(params.primary_id) })),
    },

    // --- DNS TLSA records (4 new) ---
    {
      name: "isp_dns_tlsa_get",
      description: "Get a single DNS TLSA record by ID",
      parameters: {
        type: "object" as const,
        properties: {
          primary_id: { type: "number", description: "DNS record ID" },
        },
        required: ["primary_id"],
      },
      run: async (params, context) => withClient(context, "isp_dns_tlsa_get", (client) =>
        client.call("dns_tlsa_get", { primary_id: toNumber(params.primary_id) })),
    },
    {
      name: "isp_dns_tlsa_add",
      description: "Add a DNS TLSA record",
      parameters: {
        type: "object" as const,
        properties: {
          client_id: { type: "number", description: "Client ID" },
          params: { type: "object", description: "DNS TLSA record parameters" },
        },
        required: ["client_id", "params"],
      },
      run: async (params, context) => withClient(context, "isp_dns_tlsa_add", (client) =>
        client.call("dns_tlsa_add", params)),
    },
    {
      name: "isp_dns_tlsa_update",
      description: "Update a DNS TLSA record",
      parameters: {
        type: "object" as const,
        properties: {
          client_id: { type: "number", description: "Client ID" },
          primary_id: { type: "number", description: "DNS record ID to update" },
          params: { type: "object", description: "Fields to update" },
        },
        required: ["client_id", "primary_id", "params"],
      },
      run: async (params, context) => withClient(context, "isp_dns_tlsa_update", (client) =>
        client.call("dns_tlsa_update", params)),
    },
    {
      name: "isp_dns_tlsa_delete",
      description: "Delete a DNS TLSA record",
      parameters: {
        type: "object" as const,
        properties: {
          primary_id: { type: "number", description: "DNS record ID to delete" },
        },
        required: ["primary_id"],
      },
      run: async (params, context) => withClient(context, "isp_dns_tlsa_delete", (client) =>
        client.call("dns_tlsa_delete", { primary_id: toNumber(params.primary_id) })),
    },

    // --- DNS Slave Zones (4 new) ---
    {
      name: "isp_dns_slave_get",
      description: "Get a DNS slave zone by ID",
      parameters: {
        type: "object" as const,
        properties: {
          primary_id: { type: "number", description: "DNS slave zone ID" },
        },
        required: ["primary_id"],
      },
      run: async (params, context) => withClient(context, "isp_dns_slave_get", (client) =>
        client.call("dns_slave_get", { primary_id: toNumber(params.primary_id) })),
    },
    {
      name: "isp_dns_slave_add",
      description: "Add a DNS slave zone",
      parameters: {
        type: "object" as const,
        properties: {
          client_id: { type: "number", description: "Client ID" },
          params: { type: "object", description: "DNS slave zone parameters" },
        },
        required: ["client_id", "params"],
      },
      run: async (params, context) => withClient(context, "isp_dns_slave_add", (client) =>
        client.call("dns_slave_add", params)),
    },
    {
      name: "isp_dns_slave_update",
      description: "Update a DNS slave zone",
      parameters: {
        type: "object" as const,
        properties: {
          client_id: { type: "number", description: "Client ID" },
          primary_id: { type: "number", description: "DNS slave zone ID to update" },
          params: { type: "object", description: "Fields to update" },
        },
        required: ["client_id", "primary_id", "params"],
      },
      run: async (params, context) => withClient(context, "isp_dns_slave_update", (client) =>
        client.call("dns_slave_update", params)),
    },
    {
      name: "isp_dns_slave_delete",
      description: "Delete a DNS slave zone",
      parameters: {
        type: "object" as const,
        properties: {
          primary_id: { type: "number", description: "DNS slave zone ID to delete" },
        },
        required: ["primary_id"],
      },
      run: async (params, context) => withClient(context, "isp_dns_slave_delete", (client) =>
        client.call("dns_slave_delete", { primary_id: toNumber(params.primary_id) })),
    },

    // --- DNS Template Zones (2 new) ---
    {
      name: "isp_dns_templatezone_list",
      description: "List all DNS template zones",
      parameters: { type: "object" as const, properties: {} },
      run: async (_params, context) => withClient(context, "isp_dns_templatezone_list", (client) =>
        client.call("dns_templatezone_get_all", {})),
    },
    {
      name: "isp_dns_templatezone_add",
      description: "Add a DNS template zone",
      parameters: {
        type: "object" as const,
        properties: {
          client_id: { type: "number", description: "Client ID" },
          params: { type: "object", description: "DNS template zone parameters" },
        },
        required: ["client_id", "params"],
      },
      run: async (params, context) => withClient(context, "isp_dns_templatezone_add", (client) =>
        client.call("dns_templatezone_add", params)),
    },

    // --- DNS Zone Extended (3 new) ---
    {
      name: "isp_dns_zone_get_id",
      description: "Look up DNS zone ID by origin domain name",
      parameters: {
        type: "object" as const,
        properties: {
          origin: { type: "string", description: "Zone origin (e.g. example.com.)" },
        },
        required: ["origin"],
      },
      run: async (params, context) => withClient(context, "isp_dns_zone_get_id", (client) =>
        client.call("dns_zone_get_id", { origin: String(params.origin) })),
    },
    {
      name: "isp_dns_zone_set_status",
      description: "Enable or disable a DNS zone",
      parameters: {
        type: "object" as const,
        properties: {
          primary_id: { type: "number", description: "DNS zone ID" },
          status: { type: "string", enum: ["active", "inactive"], description: "New status" },
        },
        required: ["primary_id", "status"],
      },
      run: async (params, context) => withClient(context, "isp_dns_zone_set_status", (client) =>
        client.call("dns_zone_set_status", { primary_id: toNumber(params.primary_id), status: String(params.status) })),
    },
    {
      name: "isp_dns_zone_set_dnssec",
      description: "Enable or disable DNSSEC for a DNS zone",
      parameters: {
        type: "object" as const,
        properties: {
          primary_id: { type: "number", description: "DNS zone ID" },
          params: { type: "object", description: "DNSSEC parameters" },
        },
        required: ["primary_id"],
      },
      run: async (params, context) => withClient(context, "isp_dns_zone_set_dnssec", (client) =>
        client.call("dns_zone_set_dnssec", params)),
    },

    // -------------------------------------------------------------------------
    // New in v0.7.0 — Phase 3: Mail Complete
    // -------------------------------------------------------------------------

    // --- Mail Alias Domains (4 new) ---
    {
      name: "isp_mail_aliasdomain_get",
      description: "Get a mail alias domain by ID",
      parameters: {
        type: "object" as const,
        properties: {
          primary_id: { type: "number", description: "Mail alias domain ID" },
        },
        required: ["primary_id"],
      },
      run: async (params, context) => withClient(context, "isp_mail_aliasdomain_get", (client) =>
        client.call("mail_aliasdomain_get", { primary_id: toNumber(params.primary_id) })),
    },
    {
      name: "isp_mail_aliasdomain_add",
      description: "Create a mail alias domain",
      parameters: {
        type: "object" as const,
        properties: {
          client_id: { type: "number", description: "Client ID" },
          params: { type: "object", description: "Mail alias domain parameters (server_id, domain, destination_domain, active)" },
        },
        required: ["client_id", "params"],
      },
      run: async (params, context) => withClient(context, "isp_mail_aliasdomain_add", (client) =>
        client.call("mail_aliasdomain_add", params)),
    },
    {
      name: "isp_mail_aliasdomain_update",
      description: "Update a mail alias domain",
      parameters: {
        type: "object" as const,
        properties: {
          client_id: { type: "number", description: "Client ID" },
          primary_id: { type: "number", description: "Mail alias domain ID to update" },
          params: { type: "object", description: "Fields to update" },
        },
        required: ["client_id", "primary_id", "params"],
      },
      run: async (params, context) => withClient(context, "isp_mail_aliasdomain_update", (client) =>
        client.call("mail_aliasdomain_update", params)),
    },
    {
      name: "isp_mail_aliasdomain_delete",
      description: "Delete a mail alias domain",
      parameters: {
        type: "object" as const,
        properties: {
          primary_id: { type: "number", description: "Mail alias domain ID to delete" },
        },
        required: ["primary_id"],
      },
      run: async (params, context) => withClient(context, "isp_mail_aliasdomain_delete", (client) =>
        client.call("mail_aliasdomain_delete", { primary_id: toNumber(params.primary_id) })),
    },

    // --- Mail Catchall (4 new) ---
    {
      name: "isp_mail_catchall_get",
      description: "Get a mail catchall by ID",
      parameters: {
        type: "object" as const,
        properties: {
          primary_id: { type: "number", description: "Mail catchall ID" },
        },
        required: ["primary_id"],
      },
      run: async (params, context) => withClient(context, "isp_mail_catchall_get", (client) =>
        client.call("mail_catchall_get", { primary_id: toNumber(params.primary_id) })),
    },
    {
      name: "isp_mail_catchall_add",
      description: "Create a mail catchall",
      parameters: {
        type: "object" as const,
        properties: {
          client_id: { type: "number", description: "Client ID" },
          params: { type: "object", description: "Mail catchall parameters (server_id, source, destination, active)" },
        },
        required: ["client_id", "params"],
      },
      run: async (params, context) => withClient(context, "isp_mail_catchall_add", (client) =>
        client.call("mail_catchall_add", params)),
    },
    {
      name: "isp_mail_catchall_update",
      description: "Update a mail catchall",
      parameters: {
        type: "object" as const,
        properties: {
          client_id: { type: "number", description: "Client ID" },
          primary_id: { type: "number", description: "Mail catchall ID to update" },
          params: { type: "object", description: "Fields to update" },
        },
        required: ["client_id", "primary_id", "params"],
      },
      run: async (params, context) => withClient(context, "isp_mail_catchall_update", (client) =>
        client.call("mail_catchall_update", params)),
    },
    {
      name: "isp_mail_catchall_delete",
      description: "Delete a mail catchall",
      parameters: {
        type: "object" as const,
        properties: {
          primary_id: { type: "number", description: "Mail catchall ID to delete" },
        },
        required: ["primary_id"],
      },
      run: async (params, context) => withClient(context, "isp_mail_catchall_delete", (client) =>
        client.call("mail_catchall_delete", { primary_id: toNumber(params.primary_id) })),
    },

    // --- Mailing Lists (4 new) ---
    {
      name: "isp_mail_mailinglist_get",
      description: "Get a mailing list by ID",
      parameters: {
        type: "object" as const,
        properties: {
          primary_id: { type: "number", description: "Mailing list ID" },
        },
        required: ["primary_id"],
      },
      run: async (params, context) => withClient(context, "isp_mail_mailinglist_get", (client) =>
        client.call("mail_mailinglist_get", { primary_id: toNumber(params.primary_id) })),
    },
    {
      name: "isp_mail_mailinglist_add",
      description: "Create a mailing list",
      parameters: {
        type: "object" as const,
        properties: {
          client_id: { type: "number", description: "Client ID" },
          params: { type: "object", description: "Mailing list parameters (server_id, domain, listname, email, password)" },
        },
        required: ["client_id", "params"],
      },
      run: async (params, context) => withClient(context, "isp_mail_mailinglist_add", (client) =>
        client.call("mail_mailinglist_add", params)),
    },
    {
      name: "isp_mail_mailinglist_update",
      description: "Update a mailing list",
      parameters: {
        type: "object" as const,
        properties: {
          client_id: { type: "number", description: "Client ID" },
          primary_id: { type: "number", description: "Mailing list ID to update" },
          params: { type: "object", description: "Fields to update" },
        },
        required: ["client_id", "primary_id", "params"],
      },
      run: async (params, context) => withClient(context, "isp_mail_mailinglist_update", (client) =>
        client.call("mail_mailinglist_update", params)),
    },
    {
      name: "isp_mail_mailinglist_delete",
      description: "Delete a mailing list",
      parameters: {
        type: "object" as const,
        properties: {
          primary_id: { type: "number", description: "Mailing list ID to delete" },
        },
        required: ["primary_id"],
      },
      run: async (params, context) => withClient(context, "isp_mail_mailinglist_delete", (client) =>
        client.call("mail_mailinglist_delete", { primary_id: toNumber(params.primary_id) })),
    },

    // --- Mail User Filters (4 new) ---
    {
      name: "isp_mail_user_filter_get",
      description: "Get a mail user filter by ID",
      parameters: {
        type: "object" as const,
        properties: {
          primary_id: { type: "number", description: "Mail user filter ID" },
        },
        required: ["primary_id"],
      },
      run: async (params, context) => withClient(context, "isp_mail_user_filter_get", (client) =>
        client.call("mail_user_filter_get", { primary_id: toNumber(params.primary_id) })),
    },
    {
      name: "isp_mail_user_filter_add",
      description: "Create a mail user filter",
      parameters: {
        type: "object" as const,
        properties: {
          client_id: { type: "number", description: "Client ID" },
          params: { type: "object", description: "Mail user filter parameters (mailuser_id, rulename, source, searchterm, op, action, target, active)" },
        },
        required: ["client_id", "params"],
      },
      run: async (params, context) => withClient(context, "isp_mail_user_filter_add", (client) =>
        client.call("mail_user_filter_add", params)),
    },
    {
      name: "isp_mail_user_filter_update",
      description: "Update a mail user filter",
      parameters: {
        type: "object" as const,
        properties: {
          client_id: { type: "number", description: "Client ID" },
          primary_id: { type: "number", description: "Mail user filter ID to update" },
          params: { type: "object", description: "Fields to update" },
        },
        required: ["client_id", "primary_id", "params"],
      },
      run: async (params, context) => withClient(context, "isp_mail_user_filter_update", (client) =>
        client.call("mail_user_filter_update", params)),
    },
    {
      name: "isp_mail_user_filter_delete",
      description: "Delete a mail user filter",
      parameters: {
        type: "object" as const,
        properties: {
          primary_id: { type: "number", description: "Mail user filter ID to delete" },
        },
        required: ["primary_id"],
      },
      run: async (params, context) => withClient(context, "isp_mail_user_filter_delete", (client) =>
        client.call("mail_user_filter_delete", { primary_id: toNumber(params.primary_id) })),
    },

    // --- Mail User Extended (3 new) ---
    {
      name: "isp_mail_user_backup_list",
      description: "List backups for a mail user",
      parameters: {
        type: "object" as const,
        properties: {
          primary_id: { type: "number", description: "Mail user ID" },
        },
        required: ["primary_id"],
      },
      run: async (params, context) => withClient(context, "isp_mail_user_backup_list", (client) =>
        client.call("mail_user_backup_list", { primary_id: toNumber(params.primary_id) })),
    },
    {
      name: "isp_mail_user_backup",
      description: "Trigger a mail user backup",
      parameters: {
        type: "object" as const,
        properties: {
          primary_id: { type: "number", description: "Mail user ID to backup" },
          params: { type: "object", description: "Backup parameters" },
        },
        required: ["primary_id"],
      },
      run: async (params, context) => withClient(context, "isp_mail_user_backup", (client) =>
        client.call("mail_user_backup", params)),
    },
    {
      name: "isp_mail_user_list_by_client",
      description: "List all mail users for a client",
      parameters: {
        type: "object" as const,
        properties: {
          client_id: { type: "number", description: "Client ID" },
        },
        required: ["client_id"],
      },
      run: async (params, context) => withClient(context, "isp_mail_user_list_by_client", (client) =>
        client.call("mail_user_get_all_by_client", { client_id: toNumber(params.client_id) })),
    },

    // --- Mail Domain Extended (2 new) ---
    {
      name: "isp_mail_domain_get_by_domain",
      description: "Look up a mail domain by domain name",
      parameters: {
        type: "object" as const,
        properties: {
          domain: { type: "string", description: "Domain name" },
        },
        required: ["domain"],
      },
      run: async (params, context) => withClient(context, "isp_mail_domain_get_by_domain", (client) =>
        client.call("mail_domain_get_by_domain", { domain: String(params.domain) })),
    },
    {
      name: "isp_mail_domain_set_status",
      description: "Enable or disable a mail domain",
      parameters: {
        type: "object" as const,
        properties: {
          primary_id: { type: "number", description: "Mail domain ID" },
          status: { type: "string", enum: ["active", "inactive"], description: "New status" },
        },
        required: ["primary_id", "status"],
      },
      run: async (params, context) => withClient(context, "isp_mail_domain_set_status", (client) =>
        client.call("mail_domain_set_status", { primary_id: toNumber(params.primary_id), status: String(params.status) })),
    },

    // --- Mail Quota (1 new) ---
    {
      name: "isp_mail_quota_get",
      description: "Get mail quota data for a user",
      parameters: {
        type: "object" as const,
        properties: {
          client_group_id: { type: "number", description: "Client group ID" },
        },
        required: ["client_group_id"],
      },
      run: async (params, context) => withClient(context, "isp_mail_quota_get", (client) =>
        client.call("mailquota_get_by_user", { client_group_id: toNumber(params.client_group_id) })),
    },

    // --- Fetchmail (4 new) ---
    {
      name: "isp_mail_fetchmail_get",
      description: "Get a fetchmail entry by ID",
      parameters: {
        type: "object" as const,
        properties: {
          primary_id: { type: "number", description: "Fetchmail entry ID" },
        },
        required: ["primary_id"],
      },
      run: async (params, context) => withClient(context, "isp_mail_fetchmail_get", (client) =>
        client.call("mail_fetchmail_get", { primary_id: toNumber(params.primary_id) })),
    },
    {
      name: "isp_mail_fetchmail_add",
      description: "Create a fetchmail entry",
      parameters: {
        type: "object" as const,
        properties: {
          client_id: { type: "number", description: "Client ID" },
          params: { type: "object", description: "Fetchmail parameters (server_id, type, source_server, source_username, source_password, source_mailbox, destination, active)" },
        },
        required: ["client_id", "params"],
      },
      run: async (params, context) => withClient(context, "isp_mail_fetchmail_add", (client) =>
        client.call("mail_fetchmail_add", params)),
    },
    {
      name: "isp_mail_fetchmail_update",
      description: "Update a fetchmail entry",
      parameters: {
        type: "object" as const,
        properties: {
          client_id: { type: "number", description: "Client ID" },
          primary_id: { type: "number", description: "Fetchmail entry ID to update" },
          params: { type: "object", description: "Fields to update" },
        },
        required: ["client_id", "primary_id", "params"],
      },
      run: async (params, context) => withClient(context, "isp_mail_fetchmail_update", (client) =>
        client.call("mail_fetchmail_update", params)),
    },
    {
      name: "isp_mail_fetchmail_delete",
      description: "Delete a fetchmail entry",
      parameters: {
        type: "object" as const,
        properties: {
          primary_id: { type: "number", description: "Fetchmail entry ID to delete" },
        },
        required: ["primary_id"],
      },
      run: async (params, context) => withClient(context, "isp_mail_fetchmail_delete", (client) =>
        client.call("mail_fetchmail_delete", { primary_id: toNumber(params.primary_id) })),
    },

    // --- Mail Transport (4 new) ---
    {
      name: "isp_mail_transport_get",
      description: "Get a mail transport entry by ID",
      parameters: {
        type: "object" as const,
        properties: {
          primary_id: { type: "number", description: "Mail transport ID" },
        },
        required: ["primary_id"],
      },
      run: async (params, context) => withClient(context, "isp_mail_transport_get", (client) =>
        client.call("mail_transport_get", { primary_id: toNumber(params.primary_id) })),
    },
    {
      name: "isp_mail_transport_add",
      description: "Create a mail transport entry",
      parameters: {
        type: "object" as const,
        properties: {
          client_id: { type: "number", description: "Client ID" },
          params: { type: "object", description: "Mail transport parameters (server_id, domain, transport, sort_order, active)" },
        },
        required: ["client_id", "params"],
      },
      run: async (params, context) => withClient(context, "isp_mail_transport_add", (client) =>
        client.call("mail_transport_add", params)),
    },
    {
      name: "isp_mail_transport_update",
      description: "Update a mail transport entry",
      parameters: {
        type: "object" as const,
        properties: {
          client_id: { type: "number", description: "Client ID" },
          primary_id: { type: "number", description: "Mail transport ID to update" },
          params: { type: "object", description: "Fields to update" },
        },
        required: ["client_id", "primary_id", "params"],
      },
      run: async (params, context) => withClient(context, "isp_mail_transport_update", (client) =>
        client.call("mail_transport_update", params)),
    },
    {
      name: "isp_mail_transport_delete",
      description: "Delete a mail transport entry",
      parameters: {
        type: "object" as const,
        properties: {
          primary_id: { type: "number", description: "Mail transport ID to delete" },
        },
        required: ["primary_id"],
      },
      run: async (params, context) => withClient(context, "isp_mail_transport_delete", (client) =>
        client.call("mail_transport_delete", { primary_id: toNumber(params.primary_id) })),
    },

    // --- Mail Relay Recipient (4 new) ---
    {
      name: "isp_mail_relay_recipient_get",
      description: "Get a mail relay recipient by ID",
      parameters: {
        type: "object" as const,
        properties: {
          primary_id: { type: "number", description: "Mail relay recipient ID" },
        },
        required: ["primary_id"],
      },
      run: async (params, context) => withClient(context, "isp_mail_relay_recipient_get", (client) =>
        client.call("mail_relay_recipient_get", { primary_id: toNumber(params.primary_id) })),
    },
    {
      name: "isp_mail_relay_recipient_add",
      description: "Create a mail relay recipient",
      parameters: {
        type: "object" as const,
        properties: {
          client_id: { type: "number", description: "Client ID" },
          params: { type: "object", description: "Mail relay recipient parameters (server_id, source, access, active)" },
        },
        required: ["client_id", "params"],
      },
      run: async (params, context) => withClient(context, "isp_mail_relay_recipient_add", (client) =>
        client.call("mail_relay_recipient_add", params)),
    },
    {
      name: "isp_mail_relay_recipient_update",
      description: "Update a mail relay recipient",
      parameters: {
        type: "object" as const,
        properties: {
          client_id: { type: "number", description: "Client ID" },
          primary_id: { type: "number", description: "Mail relay recipient ID to update" },
          params: { type: "object", description: "Fields to update" },
        },
        required: ["client_id", "primary_id", "params"],
      },
      run: async (params, context) => withClient(context, "isp_mail_relay_recipient_update", (client) =>
        client.call("mail_relay_recipient_update", params)),
    },
    {
      name: "isp_mail_relay_recipient_delete",
      description: "Delete a mail relay recipient",
      parameters: {
        type: "object" as const,
        properties: {
          primary_id: { type: "number", description: "Mail relay recipient ID to delete" },
        },
        required: ["primary_id"],
      },
      run: async (params, context) => withClient(context, "isp_mail_relay_recipient_delete", (client) =>
        client.call("mail_relay_recipient_delete", { primary_id: toNumber(params.primary_id) })),
    },

    // --- Mail Relay Domain (4 new) ---
    {
      name: "isp_mail_relay_domain_get",
      description: "Get a mail relay domain by ID",
      parameters: {
        type: "object" as const,
        properties: {
          primary_id: { type: "number", description: "Mail relay domain ID" },
        },
        required: ["primary_id"],
      },
      run: async (params, context) => withClient(context, "isp_mail_relay_domain_get", (client) =>
        client.call("mail_relay_domain_get", { primary_id: toNumber(params.primary_id) })),
    },
    {
      name: "isp_mail_relay_domain_add",
      description: "Create a mail relay domain",
      parameters: {
        type: "object" as const,
        properties: {
          client_id: { type: "number", description: "Client ID" },
          params: { type: "object", description: "Mail relay domain parameters (server_id, domain, active)" },
        },
        required: ["client_id", "params"],
      },
      run: async (params, context) => withClient(context, "isp_mail_relay_domain_add", (client) =>
        client.call("mail_relay_domain_add", params)),
    },
    {
      name: "isp_mail_relay_domain_update",
      description: "Update a mail relay domain",
      parameters: {
        type: "object" as const,
        properties: {
          client_id: { type: "number", description: "Client ID" },
          primary_id: { type: "number", description: "Mail relay domain ID to update" },
          params: { type: "object", description: "Fields to update" },
        },
        required: ["client_id", "primary_id", "params"],
      },
      run: async (params, context) => withClient(context, "isp_mail_relay_domain_update", (client) =>
        client.call("mail_relay_domain_update", params)),
    },
    {
      name: "isp_mail_relay_domain_delete",
      description: "Delete a mail relay domain",
      parameters: {
        type: "object" as const,
        properties: {
          primary_id: { type: "number", description: "Mail relay domain ID to delete" },
        },
        required: ["primary_id"],
      },
      run: async (params, context) => withClient(context, "isp_mail_relay_domain_delete", (client) =>
        client.call("mail_relay_domain_delete", { primary_id: toNumber(params.primary_id) })),
    },

    // --- Spam Filter Whitelist (4 new) ---
    {
      name: "isp_mail_spamfilter_whitelist_get",
      description: "Get a spamfilter whitelist entry by ID",
      parameters: {
        type: "object" as const,
        properties: {
          primary_id: { type: "number", description: "Spamfilter whitelist entry ID" },
        },
        required: ["primary_id"],
      },
      run: async (params, context) => withClient(context, "isp_mail_spamfilter_whitelist_get", (client) =>
        client.call("mail_spamfilter_whitelist_get", { primary_id: toNumber(params.primary_id) })),
    },
    {
      name: "isp_mail_spamfilter_whitelist_add",
      description: "Create a spamfilter whitelist entry",
      parameters: {
        type: "object" as const,
        properties: {
          client_id: { type: "number", description: "Client ID" },
          params: { type: "object", description: "Spamfilter whitelist parameters (server_id, wb, email, priority, active)" },
        },
        required: ["client_id", "params"],
      },
      run: async (params, context) => withClient(context, "isp_mail_spamfilter_whitelist_add", (client) =>
        client.call("mail_spamfilter_whitelist_add", params)),
    },
    {
      name: "isp_mail_spamfilter_whitelist_update",
      description: "Update a spamfilter whitelist entry",
      parameters: {
        type: "object" as const,
        properties: {
          client_id: { type: "number", description: "Client ID" },
          primary_id: { type: "number", description: "Spamfilter whitelist entry ID to update" },
          params: { type: "object", description: "Fields to update" },
        },
        required: ["client_id", "primary_id", "params"],
      },
      run: async (params, context) => withClient(context, "isp_mail_spamfilter_whitelist_update", (client) =>
        client.call("mail_spamfilter_whitelist_update", params)),
    },
    {
      name: "isp_mail_spamfilter_whitelist_delete",
      description: "Delete a spamfilter whitelist entry",
      parameters: {
        type: "object" as const,
        properties: {
          primary_id: { type: "number", description: "Spamfilter whitelist entry ID to delete" },
        },
        required: ["primary_id"],
      },
      run: async (params, context) => withClient(context, "isp_mail_spamfilter_whitelist_delete", (client) =>
        client.call("mail_spamfilter_whitelist_delete", { primary_id: toNumber(params.primary_id) })),
    },

    // --- Spam Filter Blacklist (4 new) ---
    {
      name: "isp_mail_spamfilter_blacklist_get",
      description: "Get a spamfilter blacklist entry by ID",
      parameters: {
        type: "object" as const,
        properties: {
          primary_id: { type: "number", description: "Spamfilter blacklist entry ID" },
        },
        required: ["primary_id"],
      },
      run: async (params, context) => withClient(context, "isp_mail_spamfilter_blacklist_get", (client) =>
        client.call("mail_spamfilter_blacklist_get", { primary_id: toNumber(params.primary_id) })),
    },
    {
      name: "isp_mail_spamfilter_blacklist_add",
      description: "Create a spamfilter blacklist entry",
      parameters: {
        type: "object" as const,
        properties: {
          client_id: { type: "number", description: "Client ID" },
          params: { type: "object", description: "Spamfilter blacklist parameters (server_id, wb, email, priority, active)" },
        },
        required: ["client_id", "params"],
      },
      run: async (params, context) => withClient(context, "isp_mail_spamfilter_blacklist_add", (client) =>
        client.call("mail_spamfilter_blacklist_add", params)),
    },
    {
      name: "isp_mail_spamfilter_blacklist_update",
      description: "Update a spamfilter blacklist entry",
      parameters: {
        type: "object" as const,
        properties: {
          client_id: { type: "number", description: "Client ID" },
          primary_id: { type: "number", description: "Spamfilter blacklist entry ID to update" },
          params: { type: "object", description: "Fields to update" },
        },
        required: ["client_id", "primary_id", "params"],
      },
      run: async (params, context) => withClient(context, "isp_mail_spamfilter_blacklist_update", (client) =>
        client.call("mail_spamfilter_blacklist_update", params)),
    },
    {
      name: "isp_mail_spamfilter_blacklist_delete",
      description: "Delete a spamfilter blacklist entry",
      parameters: {
        type: "object" as const,
        properties: {
          primary_id: { type: "number", description: "Spamfilter blacklist entry ID to delete" },
        },
        required: ["primary_id"],
      },
      run: async (params, context) => withClient(context, "isp_mail_spamfilter_blacklist_delete", (client) =>
        client.call("mail_spamfilter_blacklist_delete", { primary_id: toNumber(params.primary_id) })),
    },

    // --- Spam Filter User (4 new) ---
    {
      name: "isp_mail_spamfilter_user_get",
      description: "Get a spamfilter user entry by ID",
      parameters: {
        type: "object" as const,
        properties: {
          primary_id: { type: "number", description: "Spamfilter user entry ID" },
        },
        required: ["primary_id"],
      },
      run: async (params, context) => withClient(context, "isp_mail_spamfilter_user_get", (client) =>
        client.call("mail_spamfilter_user_get", { primary_id: toNumber(params.primary_id) })),
    },
    {
      name: "isp_mail_spamfilter_user_add",
      description: "Create a spamfilter user entry",
      parameters: {
        type: "object" as const,
        properties: {
          client_id: { type: "number", description: "Client ID" },
          params: { type: "object", description: "Spamfilter user parameters (server_id, email, policy_id, fullname, local)" },
        },
        required: ["client_id", "params"],
      },
      run: async (params, context) => withClient(context, "isp_mail_spamfilter_user_add", (client) =>
        client.call("mail_spamfilter_user_add", params)),
    },
    {
      name: "isp_mail_spamfilter_user_update",
      description: "Update a spamfilter user entry",
      parameters: {
        type: "object" as const,
        properties: {
          client_id: { type: "number", description: "Client ID" },
          primary_id: { type: "number", description: "Spamfilter user entry ID to update" },
          params: { type: "object", description: "Fields to update" },
        },
        required: ["client_id", "primary_id", "params"],
      },
      run: async (params, context) => withClient(context, "isp_mail_spamfilter_user_update", (client) =>
        client.call("mail_spamfilter_user_update", params)),
    },
    {
      name: "isp_mail_spamfilter_user_delete",
      description: "Delete a spamfilter user entry",
      parameters: {
        type: "object" as const,
        properties: {
          primary_id: { type: "number", description: "Spamfilter user entry ID to delete" },
        },
        required: ["primary_id"],
      },
      run: async (params, context) => withClient(context, "isp_mail_spamfilter_user_delete", (client) =>
        client.call("mail_spamfilter_user_delete", { primary_id: toNumber(params.primary_id) })),
    },

    // --- Mail Policy (4 new) ---
    {
      name: "isp_mail_policy_get",
      description: "Get a mail policy by ID",
      parameters: {
        type: "object" as const,
        properties: {
          primary_id: { type: "number", description: "Mail policy ID" },
        },
        required: ["primary_id"],
      },
      run: async (params, context) => withClient(context, "isp_mail_policy_get", (client) =>
        client.call("mail_policy_get", { primary_id: toNumber(params.primary_id) })),
    },
    {
      name: "isp_mail_policy_add",
      description: "Create a mail policy",
      parameters: {
        type: "object" as const,
        properties: {
          client_id: { type: "number", description: "Client ID" },
          params: { type: "object", description: "Mail policy parameters (policy_name, virus_lover, spam_lover, banned_rulenames, etc.)" },
        },
        required: ["client_id", "params"],
      },
      run: async (params, context) => withClient(context, "isp_mail_policy_add", (client) =>
        client.call("mail_policy_add", params)),
    },
    {
      name: "isp_mail_policy_update",
      description: "Update a mail policy",
      parameters: {
        type: "object" as const,
        properties: {
          client_id: { type: "number", description: "Client ID" },
          primary_id: { type: "number", description: "Mail policy ID to update" },
          params: { type: "object", description: "Fields to update" },
        },
        required: ["client_id", "primary_id", "params"],
      },
      run: async (params, context) => withClient(context, "isp_mail_policy_update", (client) =>
        client.call("mail_policy_update", params)),
    },
    {
      name: "isp_mail_policy_delete",
      description: "Delete a mail policy",
      parameters: {
        type: "object" as const,
        properties: {
          primary_id: { type: "number", description: "Mail policy ID to delete" },
        },
        required: ["primary_id"],
      },
      run: async (params, context) => withClient(context, "isp_mail_policy_delete", (client) =>
        client.call("mail_policy_delete", { primary_id: toNumber(params.primary_id) })),
    },

    // --- Mail Whitelist (4 new) ---
    {
      name: "isp_mail_whitelist_get",
      description: "Get a mail whitelist entry by ID",
      parameters: {
        type: "object" as const,
        properties: {
          primary_id: { type: "number", description: "Mail whitelist entry ID" },
        },
        required: ["primary_id"],
      },
      run: async (params, context) => withClient(context, "isp_mail_whitelist_get", (client) =>
        client.call("mail_whitelist_get", { primary_id: toNumber(params.primary_id) })),
    },
    {
      name: "isp_mail_whitelist_add",
      description: "Create a mail whitelist entry",
      parameters: {
        type: "object" as const,
        properties: {
          client_id: { type: "number", description: "Client ID" },
          params: { type: "object", description: "Mail whitelist parameters (server_id, source, access, type, active)" },
        },
        required: ["client_id", "params"],
      },
      run: async (params, context) => withClient(context, "isp_mail_whitelist_add", (client) =>
        client.call("mail_whitelist_add", params)),
    },
    {
      name: "isp_mail_whitelist_update",
      description: "Update a mail whitelist entry",
      parameters: {
        type: "object" as const,
        properties: {
          client_id: { type: "number", description: "Client ID" },
          primary_id: { type: "number", description: "Mail whitelist entry ID to update" },
          params: { type: "object", description: "Fields to update" },
        },
        required: ["client_id", "primary_id", "params"],
      },
      run: async (params, context) => withClient(context, "isp_mail_whitelist_update", (client) =>
        client.call("mail_whitelist_update", params)),
    },
    {
      name: "isp_mail_whitelist_delete",
      description: "Delete a mail whitelist entry",
      parameters: {
        type: "object" as const,
        properties: {
          primary_id: { type: "number", description: "Mail whitelist entry ID to delete" },
        },
        required: ["primary_id"],
      },
      run: async (params, context) => withClient(context, "isp_mail_whitelist_delete", (client) =>
        client.call("mail_whitelist_delete", { primary_id: toNumber(params.primary_id) })),
    },

    // --- Mail Blacklist (4 new) ---
    {
      name: "isp_mail_blacklist_get",
      description: "Get a mail blacklist entry by ID",
      parameters: {
        type: "object" as const,
        properties: {
          primary_id: { type: "number", description: "Mail blacklist entry ID" },
        },
        required: ["primary_id"],
      },
      run: async (params, context) => withClient(context, "isp_mail_blacklist_get", (client) =>
        client.call("mail_blacklist_get", { primary_id: toNumber(params.primary_id) })),
    },
    {
      name: "isp_mail_blacklist_add",
      description: "Create a mail blacklist entry",
      parameters: {
        type: "object" as const,
        properties: {
          client_id: { type: "number", description: "Client ID" },
          params: { type: "object", description: "Mail blacklist parameters (server_id, source, access, type, active)" },
        },
        required: ["client_id", "params"],
      },
      run: async (params, context) => withClient(context, "isp_mail_blacklist_add", (client) =>
        client.call("mail_blacklist_add", params)),
    },
    {
      name: "isp_mail_blacklist_update",
      description: "Update a mail blacklist entry",
      parameters: {
        type: "object" as const,
        properties: {
          client_id: { type: "number", description: "Client ID" },
          primary_id: { type: "number", description: "Mail blacklist entry ID to update" },
          params: { type: "object", description: "Fields to update" },
        },
        required: ["client_id", "primary_id", "params"],
      },
      run: async (params, context) => withClient(context, "isp_mail_blacklist_update", (client) =>
        client.call("mail_blacklist_update", params)),
    },
    {
      name: "isp_mail_blacklist_delete",
      description: "Delete a mail blacklist entry",
      parameters: {
        type: "object" as const,
        properties: {
          primary_id: { type: "number", description: "Mail blacklist entry ID to delete" },
        },
        required: ["primary_id"],
      },
      run: async (params, context) => withClient(context, "isp_mail_blacklist_delete", (client) =>
        client.call("mail_blacklist_delete", { primary_id: toNumber(params.primary_id) })),
    },

    // --- Mail Filter (4 new) ---
    {
      name: "isp_mail_filter_get",
      description: "Get a mail content filter by ID",
      parameters: {
        type: "object" as const,
        properties: {
          primary_id: { type: "number", description: "Mail filter ID" },
        },
        required: ["primary_id"],
      },
      run: async (params, context) => withClient(context, "isp_mail_filter_get", (client) =>
        client.call("mail_filter_get", { primary_id: toNumber(params.primary_id) })),
    },
    {
      name: "isp_mail_filter_add",
      description: "Create a mail content filter",
      parameters: {
        type: "object" as const,
        properties: {
          client_id: { type: "number", description: "Client ID" },
          params: { type: "object", description: "Mail filter parameters (server_id, type, pattern, data, action, active)" },
        },
        required: ["client_id", "params"],
      },
      run: async (params, context) => withClient(context, "isp_mail_filter_add", (client) =>
        client.call("mail_filter_add", params)),
    },
    {
      name: "isp_mail_filter_update",
      description: "Update a mail content filter",
      parameters: {
        type: "object" as const,
        properties: {
          client_id: { type: "number", description: "Client ID" },
          primary_id: { type: "number", description: "Mail filter ID to update" },
          params: { type: "object", description: "Fields to update" },
        },
        required: ["client_id", "primary_id", "params"],
      },
      run: async (params, context) => withClient(context, "isp_mail_filter_update", (client) =>
        client.call("mail_filter_update", params)),
    },
    {
      name: "isp_mail_filter_delete",
      description: "Delete a mail content filter",
      parameters: {
        type: "object" as const,
        properties: {
          primary_id: { type: "number", description: "Mail filter ID to delete" },
        },
        required: ["primary_id"],
      },
      run: async (params, context) => withClient(context, "isp_mail_filter_delete", (client) =>
        client.call("mail_filter_delete", { primary_id: toNumber(params.primary_id) })),
    },

    // ═══════════════════════════════════════════════════════════════
    //  Phase 4: Web Extended
    // ═══════════════════════════════════════════════════════════════

    // --- VHost Alias Domains (4) ---
    {
      name: "isp_vhost_aliasdomain_get",
      description: "Get a vhost alias domain by ID",
      parameters: {
        type: "object" as const,
        properties: {
          primary_id: { type: "number", description: "VHost alias domain ID" },
        },
        required: ["primary_id"],
      },
      run: async (params, context) => withClient(context, "isp_vhost_aliasdomain_get", (client) =>
        client.call("sites_web_vhost_aliasdomain_get", { primary_id: toNumber(params.primary_id) })),
    },
    {
      name: "isp_vhost_aliasdomain_add",
      description: "Create a vhost alias domain",
      parameters: {
        type: "object" as const,
        properties: {
          client_id: { type: "number", description: "Client ID" },
          params: { type: "object", description: "VHost alias domain parameters (server_id, domain, parent_domain_id, web_folder, active)" },
        },
        required: ["client_id", "params"],
      },
      run: async (params, context) => withClient(context, "isp_vhost_aliasdomain_add", (client) =>
        client.call("sites_web_vhost_aliasdomain_add", params)),
    },
    {
      name: "isp_vhost_aliasdomain_update",
      description: "Update a vhost alias domain",
      parameters: {
        type: "object" as const,
        properties: {
          client_id: { type: "number", description: "Client ID" },
          primary_id: { type: "number", description: "VHost alias domain ID to update" },
          params: { type: "object", description: "Fields to update" },
        },
        required: ["client_id", "primary_id", "params"],
      },
      run: async (params, context) => withClient(context, "isp_vhost_aliasdomain_update", (client) =>
        client.call("sites_web_vhost_aliasdomain_update", params)),
    },
    {
      name: "isp_vhost_aliasdomain_delete",
      description: "Delete a vhost alias domain",
      parameters: {
        type: "object" as const,
        properties: {
          primary_id: { type: "number", description: "VHost alias domain ID to delete" },
        },
        required: ["primary_id"],
      },
      run: async (params, context) => withClient(context, "isp_vhost_aliasdomain_delete", (client) =>
        client.call("sites_web_vhost_aliasdomain_delete", { primary_id: toNumber(params.primary_id) })),
    },

    // --- VHost Subdomains (4) ---
    {
      name: "isp_vhost_subdomain_get",
      description: "Get a vhost subdomain by ID",
      parameters: {
        type: "object" as const,
        properties: {
          primary_id: { type: "number", description: "VHost subdomain ID" },
        },
        required: ["primary_id"],
      },
      run: async (params, context) => withClient(context, "isp_vhost_subdomain_get", (client) =>
        client.call("sites_web_vhost_subdomain_get", { primary_id: toNumber(params.primary_id) })),
    },
    {
      name: "isp_vhost_subdomain_add",
      description: "Create a vhost subdomain",
      parameters: {
        type: "object" as const,
        properties: {
          client_id: { type: "number", description: "Client ID" },
          params: { type: "object", description: "VHost subdomain parameters (server_id, domain, parent_domain_id, web_folder, active)" },
        },
        required: ["client_id", "params"],
      },
      run: async (params, context) => withClient(context, "isp_vhost_subdomain_add", (client) =>
        client.call("sites_web_vhost_subdomain_add", params)),
    },
    {
      name: "isp_vhost_subdomain_update",
      description: "Update a vhost subdomain",
      parameters: {
        type: "object" as const,
        properties: {
          client_id: { type: "number", description: "Client ID" },
          primary_id: { type: "number", description: "VHost subdomain ID to update" },
          params: { type: "object", description: "Fields to update" },
        },
        required: ["client_id", "primary_id", "params"],
      },
      run: async (params, context) => withClient(context, "isp_vhost_subdomain_update", (client) =>
        client.call("sites_web_vhost_subdomain_update", params)),
    },
    {
      name: "isp_vhost_subdomain_delete",
      description: "Delete a vhost subdomain",
      parameters: {
        type: "object" as const,
        properties: {
          primary_id: { type: "number", description: "VHost subdomain ID to delete" },
        },
        required: ["primary_id"],
      },
      run: async (params, context) => withClient(context, "isp_vhost_subdomain_delete", (client) =>
        client.call("sites_web_vhost_subdomain_delete", { primary_id: toNumber(params.primary_id) })),
    },

    // --- Web Alias Domains (4) ---
    {
      name: "isp_web_aliasdomain_get",
      description: "Get a web alias domain by ID",
      parameters: {
        type: "object" as const,
        properties: {
          primary_id: { type: "number", description: "Web alias domain ID" },
        },
        required: ["primary_id"],
      },
      run: async (params, context) => withClient(context, "isp_web_aliasdomain_get", (client) =>
        client.call("sites_web_aliasdomain_get", { primary_id: toNumber(params.primary_id) })),
    },
    {
      name: "isp_web_aliasdomain_add",
      description: "Create a web alias domain",
      parameters: {
        type: "object" as const,
        properties: {
          client_id: { type: "number", description: "Client ID" },
          params: { type: "object", description: "Web alias domain parameters (server_id, domain, parent_domain_id, redirect_type, redirect_path, active)" },
        },
        required: ["client_id", "params"],
      },
      run: async (params, context) => withClient(context, "isp_web_aliasdomain_add", (client) =>
        client.call("sites_web_aliasdomain_add", params)),
    },
    {
      name: "isp_web_aliasdomain_update",
      description: "Update a web alias domain",
      parameters: {
        type: "object" as const,
        properties: {
          client_id: { type: "number", description: "Client ID" },
          primary_id: { type: "number", description: "Web alias domain ID to update" },
          params: { type: "object", description: "Fields to update" },
        },
        required: ["client_id", "primary_id", "params"],
      },
      run: async (params, context) => withClient(context, "isp_web_aliasdomain_update", (client) =>
        client.call("sites_web_aliasdomain_update", params)),
    },
    {
      name: "isp_web_aliasdomain_delete",
      description: "Delete a web alias domain",
      parameters: {
        type: "object" as const,
        properties: {
          primary_id: { type: "number", description: "Web alias domain ID to delete" },
        },
        required: ["primary_id"],
      },
      run: async (params, context) => withClient(context, "isp_web_aliasdomain_delete", (client) =>
        client.call("sites_web_aliasdomain_delete", { primary_id: toNumber(params.primary_id) })),
    },

    // --- Web Subdomains (4) ---
    {
      name: "isp_web_subdomain_get",
      description: "Get a web subdomain by ID",
      parameters: {
        type: "object" as const,
        properties: {
          primary_id: { type: "number", description: "Web subdomain ID" },
        },
        required: ["primary_id"],
      },
      run: async (params, context) => withClient(context, "isp_web_subdomain_get", (client) =>
        client.call("sites_web_subdomain_get", { primary_id: toNumber(params.primary_id) })),
    },
    {
      name: "isp_web_subdomain_add",
      description: "Create a web subdomain",
      parameters: {
        type: "object" as const,
        properties: {
          client_id: { type: "number", description: "Client ID" },
          params: { type: "object", description: "Web subdomain parameters (server_id, domain, parent_domain_id, redirect_type, redirect_path, active)" },
        },
        required: ["client_id", "params"],
      },
      run: async (params, context) => withClient(context, "isp_web_subdomain_add", (client) =>
        client.call("sites_web_subdomain_add", params)),
    },
    {
      name: "isp_web_subdomain_update",
      description: "Update a web subdomain",
      parameters: {
        type: "object" as const,
        properties: {
          client_id: { type: "number", description: "Client ID" },
          primary_id: { type: "number", description: "Web subdomain ID to update" },
          params: { type: "object", description: "Fields to update" },
        },
        required: ["client_id", "primary_id", "params"],
      },
      run: async (params, context) => withClient(context, "isp_web_subdomain_update", (client) =>
        client.call("sites_web_subdomain_update", params)),
    },
    {
      name: "isp_web_subdomain_delete",
      description: "Delete a web subdomain",
      parameters: {
        type: "object" as const,
        properties: {
          primary_id: { type: "number", description: "Web subdomain ID to delete" },
        },
        required: ["primary_id"],
      },
      run: async (params, context) => withClient(context, "isp_web_subdomain_delete", (client) =>
        client.call("sites_web_subdomain_delete", { primary_id: toNumber(params.primary_id) })),
    },

    // --- Web Folders (4) ---
    {
      name: "isp_web_folder_get",
      description: "Get a web folder by ID",
      parameters: {
        type: "object" as const,
        properties: {
          primary_id: { type: "number", description: "Web folder ID" },
        },
        required: ["primary_id"],
      },
      run: async (params, context) => withClient(context, "isp_web_folder_get", (client) =>
        client.call("sites_web_folder_get", { primary_id: toNumber(params.primary_id) })),
    },
    {
      name: "isp_web_folder_add",
      description: "Create a web folder (protected directory)",
      parameters: {
        type: "object" as const,
        properties: {
          client_id: { type: "number", description: "Client ID" },
          params: { type: "object", description: "Web folder parameters (server_id, parent_domain_id, path, active)" },
        },
        required: ["client_id", "params"],
      },
      run: async (params, context) => withClient(context, "isp_web_folder_add", (client) =>
        client.call("sites_web_folder_add", params)),
    },
    {
      name: "isp_web_folder_update",
      description: "Update a web folder",
      parameters: {
        type: "object" as const,
        properties: {
          client_id: { type: "number", description: "Client ID" },
          primary_id: { type: "number", description: "Web folder ID to update" },
          params: { type: "object", description: "Fields to update" },
        },
        required: ["client_id", "primary_id", "params"],
      },
      run: async (params, context) => withClient(context, "isp_web_folder_update", (client) =>
        client.call("sites_web_folder_update", params)),
    },
    {
      name: "isp_web_folder_delete",
      description: "Delete a web folder",
      parameters: {
        type: "object" as const,
        properties: {
          primary_id: { type: "number", description: "Web folder ID to delete" },
        },
        required: ["primary_id"],
      },
      run: async (params, context) => withClient(context, "isp_web_folder_delete", (client) =>
        client.call("sites_web_folder_delete", { primary_id: toNumber(params.primary_id) })),
    },

    // --- Web Folder Users (4) ---
    {
      name: "isp_web_folder_user_get",
      description: "Get a web folder user by ID",
      parameters: {
        type: "object" as const,
        properties: {
          primary_id: { type: "number", description: "Web folder user ID" },
        },
        required: ["primary_id"],
      },
      run: async (params, context) => withClient(context, "isp_web_folder_user_get", (client) =>
        client.call("sites_web_folder_user_get", { primary_id: toNumber(params.primary_id) })),
    },
    {
      name: "isp_web_folder_user_add",
      description: "Create a web folder user",
      parameters: {
        type: "object" as const,
        properties: {
          client_id: { type: "number", description: "Client ID" },
          params: { type: "object", description: "Web folder user parameters (server_id, web_folder_id, username, password, active)" },
        },
        required: ["client_id", "params"],
      },
      run: async (params, context) => withClient(context, "isp_web_folder_user_add", (client) =>
        client.call("sites_web_folder_user_add", params)),
    },
    {
      name: "isp_web_folder_user_update",
      description: "Update a web folder user",
      parameters: {
        type: "object" as const,
        properties: {
          client_id: { type: "number", description: "Client ID" },
          primary_id: { type: "number", description: "Web folder user ID to update" },
          params: { type: "object", description: "Fields to update" },
        },
        required: ["client_id", "primary_id", "params"],
      },
      run: async (params, context) => withClient(context, "isp_web_folder_user_update", (client) =>
        client.call("sites_web_folder_user_update", params)),
    },
    {
      name: "isp_web_folder_user_delete",
      description: "Delete a web folder user",
      parameters: {
        type: "object" as const,
        properties: {
          primary_id: { type: "number", description: "Web folder user ID to delete" },
        },
        required: ["primary_id"],
      },
      run: async (params, context) => withClient(context, "isp_web_folder_user_delete", (client) =>
        client.call("sites_web_folder_user_delete", { primary_id: toNumber(params.primary_id) })),
    },

    // --- WebDAV Users (4) ---
    {
      name: "isp_webdav_user_get",
      description: "Get a WebDAV user by ID",
      parameters: {
        type: "object" as const,
        properties: {
          primary_id: { type: "number", description: "WebDAV user ID" },
        },
        required: ["primary_id"],
      },
      run: async (params, context) => withClient(context, "isp_webdav_user_get", (client) =>
        client.call("sites_webdav_user_get", { primary_id: toNumber(params.primary_id) })),
    },
    {
      name: "isp_webdav_user_add",
      description: "Create a WebDAV user",
      parameters: {
        type: "object" as const,
        properties: {
          client_id: { type: "number", description: "Client ID" },
          params: { type: "object", description: "WebDAV user parameters (server_id, parent_domain_id, username, password, dir, active)" },
        },
        required: ["client_id", "params"],
      },
      run: async (params, context) => withClient(context, "isp_webdav_user_add", (client) =>
        client.call("sites_webdav_user_add", params)),
    },
    {
      name: "isp_webdav_user_update",
      description: "Update a WebDAV user",
      parameters: {
        type: "object" as const,
        properties: {
          client_id: { type: "number", description: "Client ID" },
          primary_id: { type: "number", description: "WebDAV user ID to update" },
          params: { type: "object", description: "Fields to update" },
        },
        required: ["client_id", "primary_id", "params"],
      },
      run: async (params, context) => withClient(context, "isp_webdav_user_update", (client) =>
        client.call("sites_webdav_user_update", params)),
    },
    {
      name: "isp_webdav_user_delete",
      description: "Delete a WebDAV user",
      parameters: {
        type: "object" as const,
        properties: {
          primary_id: { type: "number", description: "WebDAV user ID to delete" },
        },
        required: ["primary_id"],
      },
      run: async (params, context) => withClient(context, "isp_webdav_user_delete", (client) =>
        client.call("sites_webdav_user_delete", { primary_id: toNumber(params.primary_id) })),
    },

    // --- FTP Extended (1) ---
    {
      name: "isp_ftp_user_server_get",
      description: "Get FTP user by server (server-scoped lookup)",
      parameters: {
        type: "object" as const,
        properties: {
          primary_id: { type: "number", description: "FTP user ID" },
        },
        required: ["primary_id"],
      },
      run: async (params, context) => withClient(context, "isp_ftp_user_server_get", (client) =>
        client.call("sites_ftp_user_server_get", { primary_id: toNumber(params.primary_id) })),
    },

    // =====================================================================
    // Phase 5: System & Advanced
    // =====================================================================

    // --- System Config (2) ---
    {
      name: "isp_system_config_get",
      description: "Get ISPConfig system configuration",
      parameters: {
        type: "object" as const,
        properties: {
          section: { type: "string", description: "Config section to retrieve (e.g. 'global', 'mail', 'dns')" },
        },
        required: ["section"],
      },
      run: async (params, context) => withClient(context, "isp_system_config_get", (client) =>
        client.call("system_config_get", { section: String(params.section) })),
    },
    {
      name: "isp_system_config_set",
      description: "Set ISPConfig system configuration values",
      parameters: {
        type: "object" as const,
        properties: {
          section: { type: "string", description: "Config section to update" },
          params: { type: "object", description: "Key-value pairs to set in the section" },
        },
        required: ["section", "params"],
      },
      run: async (params, context) => withClient(context, "isp_system_config_set", (client) =>
        client.call("system_config_set", { section: String(params.section), params: params.params })),
    },

    // --- Config Values (5) ---
    {
      name: "isp_config_value_get",
      description: "Get a config value by group and name",
      parameters: {
        type: "object" as const,
        properties: {
          group: { type: "string", description: "Config group name" },
          name: { type: "string", description: "Config value name" },
        },
        required: ["group", "name"],
      },
      run: async (params, context) => withClient(context, "isp_config_value_get", (client) =>
        client.call("config_value_get", { group: String(params.group), name: String(params.name) })),
    },
    {
      name: "isp_config_value_add",
      description: "Add a new config value",
      parameters: {
        type: "object" as const,
        properties: {
          client_id: { type: "number", description: "Client ID" },
          params: { type: "object", description: "Config value parameters (group, name, value)" },
        },
        required: ["client_id", "params"],
      },
      run: async (params, context) => withClient(context, "isp_config_value_add", (client) =>
        client.call("config_value_add", params)),
    },
    {
      name: "isp_config_value_update",
      description: "Update an existing config value",
      parameters: {
        type: "object" as const,
        properties: {
          client_id: { type: "number", description: "Client ID" },
          primary_id: { type: "number", description: "Config value ID to update" },
          params: { type: "object", description: "Fields to update" },
        },
        required: ["client_id", "primary_id", "params"],
      },
      run: async (params, context) => withClient(context, "isp_config_value_update", (client) =>
        client.call("config_value_update", params)),
    },
    {
      name: "isp_config_value_replace",
      description: "Replace a config value (upsert by group and name)",
      parameters: {
        type: "object" as const,
        properties: {
          client_id: { type: "number", description: "Client ID" },
          params: { type: "object", description: "Config value parameters (group, name, value)" },
        },
        required: ["client_id", "params"],
      },
      run: async (params, context) => withClient(context, "isp_config_value_replace", (client) =>
        client.call("config_value_replace", params)),
    },
    {
      name: "isp_config_value_delete",
      description: "Delete a config value",
      parameters: {
        type: "object" as const,
        properties: {
          primary_id: { type: "number", description: "Config value ID to delete" },
        },
        required: ["primary_id"],
      },
      run: async (params, context) => withClient(context, "isp_config_value_delete", (client) =>
        client.call("config_value_delete", { primary_id: toNumber(params.primary_id) })),
    },

    // --- System Datalog (2) ---
    {
      name: "isp_datalog_get",
      description: "Get system datalog entries by ID",
      parameters: {
        type: "object" as const,
        properties: {
          primary_id: { type: "number", description: "Datalog entry ID" },
        },
        required: ["primary_id"],
      },
      run: async (params, context) => withClient(context, "isp_datalog_get", (client) =>
        client.call("sys_datalog_get", { primary_id: toNumber(params.primary_id) })),
    },
    {
      name: "isp_datalog_get_by_tstamp",
      description: "Get system datalog entries since a timestamp",
      parameters: {
        type: "object" as const,
        properties: {
          tstamp: { type: "number", description: "Unix timestamp to retrieve entries since" },
        },
        required: ["tstamp"],
      },
      run: async (params, context) => withClient(context, "isp_datalog_get_by_tstamp", (client) =>
        client.call("sys_datalog_get_by_tstamp", { tstamp: toNumber(params.tstamp) })),
    },

    // --- APS Packages (10) ---
    {
      name: "isp_aps_packages_list",
      description: "List available APS packages",
      parameters: { type: "object" as const, properties: {} },
      run: async (_params, context) => withClient(context, "isp_aps_packages_list", (client) =>
        client.call("sites_aps_available_packages_list", {})),
    },
    {
      name: "isp_aps_package_details",
      description: "Get details of an APS package",
      parameters: {
        type: "object" as const,
        properties: {
          primary_id: { type: "number", description: "APS package ID" },
        },
        required: ["primary_id"],
      },
      run: async (params, context) => withClient(context, "isp_aps_package_details", (client) =>
        client.call("sites_aps_get_package_details", { primary_id: toNumber(params.primary_id) })),
    },
    {
      name: "isp_aps_package_file",
      description: "Get the package file/metadata of an APS package",
      parameters: {
        type: "object" as const,
        properties: {
          primary_id: { type: "number", description: "APS package ID" },
        },
        required: ["primary_id"],
      },
      run: async (params, context) => withClient(context, "isp_aps_package_file", (client) =>
        client.call("sites_aps_get_package_file", { primary_id: toNumber(params.primary_id) })),
    },
    {
      name: "isp_aps_package_settings",
      description: "Get the settings/configuration options of an APS package",
      parameters: {
        type: "object" as const,
        properties: {
          primary_id: { type: "number", description: "APS package ID" },
        },
        required: ["primary_id"],
      },
      run: async (params, context) => withClient(context, "isp_aps_package_settings", (client) =>
        client.call("sites_aps_get_package_settings", { primary_id: toNumber(params.primary_id) })),
    },
    {
      name: "isp_aps_update_packages",
      description: "Update/refresh the APS package list from upstream",
      parameters: { type: "object" as const, properties: {} },
      run: async (_params, context) => withClient(context, "isp_aps_update_packages", (client) =>
        client.call("sites_aps_update_package_list", {})),
    },
    {
      name: "isp_aps_change_status",
      description: "Change the status of an APS package (enable/disable)",
      parameters: {
        type: "object" as const,
        properties: {
          primary_id: { type: "number", description: "APS package ID" },
          params: { type: "object", description: "Status parameters (e.g. { package_status: 'enabled' })" },
        },
        required: ["primary_id", "params"],
      },
      run: async (params, context) => withClient(context, "isp_aps_change_status", (client) =>
        client.call("sites_aps_change_package_status", { primary_id: toNumber(params.primary_id), params: params.params })),
    },
    {
      name: "isp_aps_install",
      description: "Install an APS package on a site",
      parameters: {
        type: "object" as const,
        properties: {
          client_id: { type: "number", description: "Client ID" },
          params: { type: "object", description: "Installation parameters (package_id, server_id, customer_id, settings, etc.)" },
        },
        required: ["client_id", "params"],
      },
      run: async (params, context) => withClient(context, "isp_aps_install", (client) =>
        client.call("sites_aps_install_package", params)),
    },
    {
      name: "isp_aps_instance_get",
      description: "Get an APS instance by ID",
      parameters: {
        type: "object" as const,
        properties: {
          primary_id: { type: "number", description: "APS instance ID" },
        },
        required: ["primary_id"],
      },
      run: async (params, context) => withClient(context, "isp_aps_instance_get", (client) =>
        client.call("sites_aps_instance_get", { primary_id: toNumber(params.primary_id) })),
    },
    {
      name: "isp_aps_instance_settings",
      description: "Get the settings of an APS instance",
      parameters: {
        type: "object" as const,
        properties: {
          primary_id: { type: "number", description: "APS instance ID" },
        },
        required: ["primary_id"],
      },
      run: async (params, context) => withClient(context, "isp_aps_instance_settings", (client) =>
        client.call("sites_aps_instance_settings_get", { primary_id: toNumber(params.primary_id) })),
    },
    {
      name: "isp_aps_instance_delete",
      description: "Delete an APS instance",
      parameters: {
        type: "object" as const,
        properties: {
          primary_id: { type: "number", description: "APS instance ID to delete" },
        },
        required: ["primary_id"],
      },
      run: async (params, context) => withClient(context, "isp_aps_instance_delete", (client) =>
        client.call("sites_aps_instance_delete", { primary_id: toNumber(params.primary_id) })),
    },

    // --- Domain Registry (5) ---
    {
      name: "isp_domain_registry_get",
      description: "Get a domain registry entry by ID",
      parameters: {
        type: "object" as const,
        properties: {
          primary_id: { type: "number", description: "Domain registry ID" },
        },
        required: ["primary_id"],
      },
      run: async (params, context) => withClient(context, "isp_domain_registry_get", (client) =>
        client.call("domains_domain_get", { primary_id: toNumber(params.primary_id) })),
    },
    {
      name: "isp_domain_registry_add",
      description: "Add a domain to the domain registry",
      parameters: {
        type: "object" as const,
        properties: {
          client_id: { type: "number", description: "Client ID" },
          params: { type: "object", description: "Domain parameters (domain name, etc.)" },
        },
        required: ["client_id", "params"],
      },
      run: async (params, context) => withClient(context, "isp_domain_registry_add", (client) =>
        client.call("domains_domain_add", params)),
    },
    {
      name: "isp_domain_registry_update",
      description: "Update a domain registry entry",
      parameters: {
        type: "object" as const,
        properties: {
          client_id: { type: "number", description: "Client ID" },
          primary_id: { type: "number", description: "Domain registry ID to update" },
          params: { type: "object", description: "Fields to update" },
        },
        required: ["client_id", "primary_id", "params"],
      },
      run: async (params, context) => withClient(context, "isp_domain_registry_update", (client) =>
        client.call("domains_domain_update", params)),
    },
    {
      name: "isp_domain_registry_delete",
      description: "Delete a domain from the domain registry",
      parameters: {
        type: "object" as const,
        properties: {
          primary_id: { type: "number", description: "Domain registry ID to delete" },
        },
        required: ["primary_id"],
      },
      run: async (params, context) => withClient(context, "isp_domain_registry_delete", (client) =>
        client.call("domains_domain_delete", { primary_id: toNumber(params.primary_id) })),
    },
    {
      name: "isp_domain_registry_list",
      description: "List all domains in the registry for a user/client",
      parameters: {
        type: "object" as const,
        properties: {
          client_id: { type: "number", description: "Client/user ID to list domains for" },
        },
        required: ["client_id"],
      },
      run: async (params, context) => withClient(context, "isp_domain_registry_list", (client) =>
        client.call("domains_get_all_by_user", { client_id: toNumber(params.client_id) })),
    },

    // =====================================================================
    // Phase 6: OpenVZ Legacy
    // =====================================================================

    // --- OpenVZ OS Templates (4) ---
    {
      name: "isp_openvz_ostemplate_get",
      description: "Get an OpenVZ OS template by ID",
      parameters: {
        type: "object" as const,
        properties: {
          primary_id: { type: "number", description: "OpenVZ OS template ID" },
        },
        required: ["primary_id"],
      },
      run: async (params, context) => withClient(context, "isp_openvz_ostemplate_get", (client) =>
        client.call("openvz_ostemplate_get", { primary_id: toNumber(params.primary_id) })),
    },
    {
      name: "isp_openvz_ostemplate_add",
      description: "Add a new OpenVZ OS template",
      parameters: {
        type: "object" as const,
        properties: {
          client_id: { type: "number", description: "Client ID" },
          params: { type: "object", description: "OS template parameters (template_name, server_id, allservers, active, description, etc.)" },
        },
        required: ["client_id", "params"],
      },
      run: async (params, context) => withClient(context, "isp_openvz_ostemplate_add", (client) =>
        client.call("openvz_ostemplate_add", params)),
    },
    {
      name: "isp_openvz_ostemplate_update",
      description: "Update an OpenVZ OS template",
      parameters: {
        type: "object" as const,
        properties: {
          client_id: { type: "number", description: "Client ID" },
          primary_id: { type: "number", description: "OS template ID to update" },
          params: { type: "object", description: "Fields to update" },
        },
        required: ["client_id", "primary_id", "params"],
      },
      run: async (params, context) => withClient(context, "isp_openvz_ostemplate_update", (client) =>
        client.call("openvz_ostemplate_update", params)),
    },
    {
      name: "isp_openvz_ostemplate_delete",
      description: "Delete an OpenVZ OS template",
      parameters: {
        type: "object" as const,
        properties: {
          primary_id: { type: "number", description: "OS template ID to delete" },
        },
        required: ["primary_id"],
      },
      run: async (params, context) => withClient(context, "isp_openvz_ostemplate_delete", (client) =>
        client.call("openvz_ostemplate_delete", { primary_id: toNumber(params.primary_id) })),
    },

    // --- OpenVZ VM Templates (4) ---
    {
      name: "isp_openvz_template_get",
      description: "Get an OpenVZ VM template by ID",
      parameters: {
        type: "object" as const,
        properties: {
          primary_id: { type: "number", description: "OpenVZ VM template ID" },
        },
        required: ["primary_id"],
      },
      run: async (params, context) => withClient(context, "isp_openvz_template_get", (client) =>
        client.call("openvz_template_get", { primary_id: toNumber(params.primary_id) })),
    },
    {
      name: "isp_openvz_template_add",
      description: "Add a new OpenVZ VM template",
      parameters: {
        type: "object" as const,
        properties: {
          client_id: { type: "number", description: "Client ID" },
          params: { type: "object", description: "VM template parameters (template_name, ostemplate_id, diskspace, ram, ram_burst, cpu_num, cpu_units, cpu_limit, etc.)" },
        },
        required: ["client_id", "params"],
      },
      run: async (params, context) => withClient(context, "isp_openvz_template_add", (client) =>
        client.call("openvz_template_add", params)),
    },
    {
      name: "isp_openvz_template_update",
      description: "Update an OpenVZ VM template",
      parameters: {
        type: "object" as const,
        properties: {
          client_id: { type: "number", description: "Client ID" },
          primary_id: { type: "number", description: "VM template ID to update" },
          params: { type: "object", description: "Fields to update" },
        },
        required: ["client_id", "primary_id", "params"],
      },
      run: async (params, context) => withClient(context, "isp_openvz_template_update", (client) =>
        client.call("openvz_template_update", params)),
    },
    {
      name: "isp_openvz_template_delete",
      description: "Delete an OpenVZ VM template",
      parameters: {
        type: "object" as const,
        properties: {
          primary_id: { type: "number", description: "VM template ID to delete" },
        },
        required: ["primary_id"],
      },
      run: async (params, context) => withClient(context, "isp_openvz_template_delete", (client) =>
        client.call("openvz_template_delete", { primary_id: toNumber(params.primary_id) })),
    },

    // --- OpenVZ IPs (5) ---
    {
      name: "isp_openvz_ip_get",
      description: "Get an OpenVZ IP address entry by ID",
      parameters: {
        type: "object" as const,
        properties: {
          primary_id: { type: "number", description: "OpenVZ IP ID" },
        },
        required: ["primary_id"],
      },
      run: async (params, context) => withClient(context, "isp_openvz_ip_get", (client) =>
        client.call("openvz_ip_get", { primary_id: toNumber(params.primary_id) })),
    },
    {
      name: "isp_openvz_ip_free",
      description: "Get a free (unassigned) OpenVZ IP address",
      parameters: {
        type: "object" as const,
        properties: {
          server_id: { type: "number", description: "Server ID to find free IP on" },
        },
        required: ["server_id"],
      },
      run: async (params, context) => withClient(context, "isp_openvz_ip_free", (client) =>
        client.call("openvz_get_free_ip", { server_id: toNumber(params.server_id) })),
    },
    {
      name: "isp_openvz_ip_add",
      description: "Add an OpenVZ IP address",
      parameters: {
        type: "object" as const,
        properties: {
          client_id: { type: "number", description: "Client ID" },
          params: { type: "object", description: "IP parameters (server_id, ip_address, vm_id, reserved, etc.)" },
        },
        required: ["client_id", "params"],
      },
      run: async (params, context) => withClient(context, "isp_openvz_ip_add", (client) =>
        client.call("openvz_ip_add", params)),
    },
    {
      name: "isp_openvz_ip_update",
      description: "Update an OpenVZ IP address entry",
      parameters: {
        type: "object" as const,
        properties: {
          client_id: { type: "number", description: "Client ID" },
          primary_id: { type: "number", description: "IP entry ID to update" },
          params: { type: "object", description: "Fields to update" },
        },
        required: ["client_id", "primary_id", "params"],
      },
      run: async (params, context) => withClient(context, "isp_openvz_ip_update", (client) =>
        client.call("openvz_ip_update", params)),
    },
    {
      name: "isp_openvz_ip_delete",
      description: "Delete an OpenVZ IP address entry",
      parameters: {
        type: "object" as const,
        properties: {
          primary_id: { type: "number", description: "IP entry ID to delete" },
        },
        required: ["primary_id"],
      },
      run: async (params, context) => withClient(context, "isp_openvz_ip_delete", (client) =>
        client.call("openvz_ip_delete", { primary_id: toNumber(params.primary_id) })),
    },

    // --- OpenVZ VMs (9) ---
    {
      name: "isp_openvz_vm_get",
      description: "Get an OpenVZ virtual machine by ID",
      parameters: {
        type: "object" as const,
        properties: {
          primary_id: { type: "number", description: "OpenVZ VM ID" },
        },
        required: ["primary_id"],
      },
      run: async (params, context) => withClient(context, "isp_openvz_vm_get", (client) =>
        client.call("openvz_vm_get", { primary_id: toNumber(params.primary_id) })),
    },
    {
      name: "isp_openvz_vm_get_by_client",
      description: "Get all OpenVZ VMs belonging to a client",
      parameters: {
        type: "object" as const,
        properties: {
          client_id: { type: "number", description: "Client ID" },
        },
        required: ["client_id"],
      },
      run: async (params, context) => withClient(context, "isp_openvz_vm_get_by_client", (client) =>
        client.call("openvz_vm_get_by_client", { client_id: toNumber(params.client_id) })),
    },
    {
      name: "isp_openvz_vm_add",
      description: "Create a new OpenVZ virtual machine",
      parameters: {
        type: "object" as const,
        properties: {
          client_id: { type: "number", description: "Client ID" },
          params: { type: "object", description: "VM parameters (server_id, ostemplate_id, template_id, hostname, ip_address, diskspace, ram, etc.)" },
        },
        required: ["client_id", "params"],
      },
      run: async (params, context) => withClient(context, "isp_openvz_vm_add", (client) =>
        client.call("openvz_vm_add", params)),
    },
    {
      name: "isp_openvz_vm_add_from_template",
      description: "Create a new OpenVZ VM from a VM template",
      parameters: {
        type: "object" as const,
        properties: {
          client_id: { type: "number", description: "Client ID" },
          params: { type: "object", description: "VM parameters including template_id to base the VM on" },
        },
        required: ["client_id", "params"],
      },
      run: async (params, context) => withClient(context, "isp_openvz_vm_add_from_template", (client) =>
        client.call("openvz_vm_add_from_template", params)),
    },
    {
      name: "isp_openvz_vm_update",
      description: "Update an OpenVZ virtual machine",
      parameters: {
        type: "object" as const,
        properties: {
          client_id: { type: "number", description: "Client ID" },
          primary_id: { type: "number", description: "VM ID to update" },
          params: { type: "object", description: "Fields to update" },
        },
        required: ["client_id", "primary_id", "params"],
      },
      run: async (params, context) => withClient(context, "isp_openvz_vm_update", (client) =>
        client.call("openvz_vm_update", params)),
    },
    {
      name: "isp_openvz_vm_delete",
      description: "Delete an OpenVZ virtual machine",
      parameters: {
        type: "object" as const,
        properties: {
          primary_id: { type: "number", description: "VM ID to delete" },
        },
        required: ["primary_id"],
      },
      run: async (params, context) => withClient(context, "isp_openvz_vm_delete", (client) =>
        client.call("openvz_vm_delete", { primary_id: toNumber(params.primary_id) })),
    },
    {
      name: "isp_openvz_vm_start",
      description: "Start an OpenVZ virtual machine",
      parameters: {
        type: "object" as const,
        properties: {
          primary_id: { type: "number", description: "VM ID to start" },
        },
        required: ["primary_id"],
      },
      run: async (params, context) => withClient(context, "isp_openvz_vm_start", (client) =>
        client.call("openvz_vm_start", { primary_id: toNumber(params.primary_id) })),
    },
    {
      name: "isp_openvz_vm_stop",
      description: "Stop an OpenVZ virtual machine",
      parameters: {
        type: "object" as const,
        properties: {
          primary_id: { type: "number", description: "VM ID to stop" },
        },
        required: ["primary_id"],
      },
      run: async (params, context) => withClient(context, "isp_openvz_vm_stop", (client) =>
        client.call("openvz_vm_stop", { primary_id: toNumber(params.primary_id) })),
    },
    {
      name: "isp_openvz_vm_restart",
      description: "Restart an OpenVZ virtual machine",
      parameters: {
        type: "object" as const,
        properties: {
          primary_id: { type: "number", description: "VM ID to restart" },
        },
        required: ["primary_id"],
      },
      run: async (params, context) => withClient(context, "isp_openvz_vm_restart", (client) =>
        client.call("openvz_vm_restart", { primary_id: toNumber(params.primary_id) })),
    },

    // --- Permissions (1) ---
    {
      name: "isp_update_record_permissions",
      description: "Update permissions on a record (change owner client/group)",
      parameters: {
        type: "object" as const,
        properties: {
          tablename: { type: "string", description: "Database table name (e.g. 'web_domain', 'mail_user')" },
          primary_id: { type: "number", description: "Record ID" },
          client_id: { type: "number", description: "New owner client ID" },
          params: { type: "object", description: "Permission parameters (sys_userid, sys_groupid, sys_perm_user, sys_perm_group, sys_perm_other)" },
        },
        required: ["tablename", "primary_id", "client_id", "params"],
      },
      run: async (params, context) => withClient(context, "isp_update_record_permissions", (client) =>
        client.call("update_record_permissions", {
          tablename: String(params.tablename),
          primary_id: toNumber(params.primary_id),
          client_id: toNumber(params.client_id),
          params: params.params,
        })),
    },
  ];

  return raw.map((tool) => ({
    ...tool,
    run: async (params: JsonMap, context: ToolContext) => {
      try {
        validateParams(tool.name, params);
        return await tool.run(params, context);
      } catch (err) {
        throw normalizeError(err);
      }
    },
  }));
}
