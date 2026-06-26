# @elvatis_com/openclaw-ispconfig

**Current version:** 1.0.0

OpenClaw plugin for full ISPConfig server management via the Remote JSON API.

## Features

- Session-based API client with auto-reconnect
- **292 tools** covering the entire ISPConfig Remote API
- Full CRUD for: Clients, Sites, DNS, Mail, Databases, FTP, Shell, Cron, WebDAV, OpenVZ
- Advanced: Spam filters, mail policies, fetchmail, relay domains, APS packages, system config
- `/ispconfig` chat command for quick help and tool reference
- Safety guards via `readOnly` and `allowedOperations`
- Live integration tests against a real ISPConfig host

## ISPConfig API format

This plugin uses the JSON endpoint format:

- URL: `https://server:8080/remote/json.php?method_name`
- Method is passed as query string, not in JSON body
- Body format:
  - login: `{ "username": "...", "password": "..." }`
  - normal calls: `{ "session_id": "...", ...params }`
  - logout: `{ "session_id": "..." }`

## Installation

### ClawHub

```bash
clawhub install openclaw-ispconfig
```

### npm

```bash
npm install @elvatis_com/openclaw-ispconfig
```

## ISPConfig setup

1. In ISPConfig, create a Remote User.
2. Grant required API permissions.
3. Copy endpoint URL and credentials.
4. Configure plugin in OpenClaw.

## Configuration

`openclaw.plugin.json` config keys:

- `apiUrl` (required): ISPConfig JSON API URL
- `username` (required): remote user
- `password` (required, secret): remote password
- `serverId` (default `1`): default server id
- `defaultServerIp` (optional): fallback IP for provisioning DNS A record
- `readOnly` (default `false`): block write tools
- `allowedOperations` (default `[]`): whitelist of tool names
- `verifySsl` (default `true`): TLS certificate verification

## Chat Command

### `/ispconfig`

Type `/ispconfig` in any connected chat to display the full list of available tools, the plugin version, and the connected ISPConfig hostname (credentials are never shown).

Example output:

```
🖥️ ISPConfig Plugin
Version 0.4.0 | Connected to isp.elvatis.com

📋 Read (17)
• isp_system_info - Server-Info
• isp_client_list - Alle Clients
...

✏️ Write (20+)
• isp_client_add / _update / _delete - Clients
...

🚀 Provisioning
• isp_provision_site - Domain + DNS + Mail + DB in einem Schritt
```

## OpenClaw Plugin API

This plugin uses the modern OpenClaw Plugin API (`api.*`) instead of the legacy `(runtime, config)` registration pattern.

The entry point exports a default plugin object with a `register(api)` function:

```ts
export default {
  manifest: pluginManifest,
  register(api: PluginApi): void {
    // Register tools
    api.registerTool({ name, description, parameters, execute });

    // Register chat commands
    api.registerCommand({ name, description, usage, handler });
  },
};
```

Key API methods used:

- `api.registerTool({ name, description, parameters, execute })` - exposes an AI-callable tool with JSON Schema parameters
- `api.registerCommand({ name, description, usage, handler })` - registers a `/command` for chat
- `api.pluginConfig` - typed plugin configuration from `openclaw.json`
- `api.logger` - structured logger (info, warn, error)

## Tools

### Read tools (22)

- `isp_system_info` - params: none
- `isp_methods_list` - params: none
- `isp_client_list` - params: optional filter fields
- `isp_client_get` - params: `client_id`
- `isp_sites_list` - params: optional filters accepted by `sites_web_domain_get`
- `isp_site_get` - params: `primary_id` (or `site_id`, `domain_id`)
- `isp_domains_list` - params: none
- `isp_dns_zone_list` - params: user-related filter params
- `isp_dns_zone_get` - params: `primary_id` (or `zone_id`)
- `isp_dns_record_list` - params: `zone_id`
- `isp_mail_domain_list` - params: optional filters
- `isp_mail_user_list` - params: optional filters
- `isp_mail_alias_list` - params: optional filters
- `isp_mail_forward_list` - params: optional filters
- `isp_db_list` - params: user-related filters
- `isp_db_get` - params: `primary_id`
- `isp_db_user_get` - params: `primary_id`
- `isp_ftp_user_get` - params: `primary_id`
- `isp_shell_user_get` - params: `primary_id`
- `isp_ssl_status` - params: none
- `isp_quota_check` - params: `client_id`
- `isp_cron_list` - params: optional filters

### Write tools (42)

- `isp_client_add` - params: ISPConfig `client_add` payload
- `isp_client_update` - params: `client_id`, `params` object with fields to update
- `isp_client_delete` - params: `client_id`
- `isp_site_add` - params: ISPConfig `sites_web_domain_add` payload
- `isp_site_update` - params: `client_id`, `primary_id`, `params` object with fields to update
- `isp_site_delete` - params: `primary_id`
- `isp_domain_add` - alias for `isp_site_add`
- `isp_dns_zone_add` - params: ISPConfig `dns_zone_add` payload
- `isp_dns_zone_update` - params: `client_id`, `primary_id`, `params` (ns, mbox, refresh, retry, expire, minimum, ttl, active)
- `isp_dns_zone_delete` - params: `primary_id`
- `isp_dns_record_add` - params: include `type` (`A`, `AAAA`, `MX`, `TXT`, `CNAME`, `SRV`, `CAA`, `NS`, `PTR`) and matching payload
- `isp_dns_record_update` - params: `type`, `primary_id`, `params` object with fields to update
- `isp_dns_record_delete` - params: include `type` and matching delete payload
- `isp_mail_domain_add` - params: ISPConfig `mail_domain_add` payload
- `isp_mail_domain_update` - params: `client_id`, `primary_id`, `params` object with fields to update
- `isp_mail_domain_delete` - params: `primary_id`
- `isp_mail_user_add` - params: ISPConfig `mail_user_add` payload
- `isp_mail_user_update` - params: `client_id`, `primary_id`, `params` (password, quota, etc.)
- `isp_mail_user_delete` - params: `primary_id`
- `isp_mail_alias_add` - params: ISPConfig `mail_alias_add` payload
- `isp_mail_alias_update` - params: `client_id`, `primary_id`, `params` object with fields to update
- `isp_mail_alias_delete` - params: `primary_id`
- `isp_mail_forward_add` - params: ISPConfig `mail_forward_add` payload
- `isp_mail_forward_update` - params: `client_id`, `primary_id`, `params` object with fields to update
- `isp_mail_forward_delete` - params: `primary_id`
- `isp_db_add` - params: ISPConfig `sites_database_add` payload
- `isp_db_update` - params: `client_id`, `primary_id`, `params` object with fields to update
- `isp_db_delete` - params: `primary_id`
- `isp_db_user_add` - params: ISPConfig `sites_database_user_add` payload
- `isp_db_user_update` - params: `client_id`, `primary_id`, `params` object with fields to update
- `isp_db_user_delete` - params: `primary_id`
- `isp_shell_user_add` - params: ISPConfig `sites_shell_user_add` payload
- `isp_shell_user_update` - params: `client_id`, `primary_id`, `params` object with fields to update
- `isp_shell_user_delete` - params: `primary_id`
- `isp_ftp_user_add` - params: ISPConfig `sites_ftp_user_add` payload
- `isp_ftp_user_update` - params: `client_id`, `primary_id`, `params` object with fields to update
- `isp_ftp_user_delete` - params: `primary_id`
- `isp_cron_add` - params: ISPConfig `sites_cron_add` payload
- `isp_cron_update` - params: `client_id`, `primary_id`, `params` object with fields to update
- `isp_cron_delete` - params: `primary_id`
- `isp_backup_list` - params: none (returns skipped if API method unavailable)

### Provisioning tool (1)

- `isp_provision_site`
- Required params:
  - `domain`
  - `clientName`
  - `clientEmail`
- Optional params:
  - `serverIp`
  - `createMail` (default `true`)
  - `createDb` (default `true`)
  - `serverId` (default from config)

Workflow:

1. Create client
2. Create site with SSL and Let's Encrypt enabled
3. Create DNS zone
4. Add DNS records (`A`, `CNAME`, SPF TXT, DMARC TXT)
5. Optionally create mail domain and `info@` + `admin@` mailboxes
6. Optionally create DB user and database
7. Ensure SSL flags are enabled on the site

**Total: 65 tools** (22 read + 42 write + 1 provisioning)

## Safety

- `readOnly=true` blocks all write and provisioning tools
- `allowedOperations=[...]` allows only named tools

## Development

```bash
npm run build
npm test
```

For live tests, provide environment variables:

- `ISPCONFIG_API_URL`
- `ISPCONFIG_USER`
- `ISPCONFIG_PASS`

## Shared Template

For automation that creates GitHub issues, use `src/templates/github-issue-helper.ts`.
It provides `isValidIssueRepoSlug()`, `resolveIssueRepo()`, and `buildGhIssueCreateCommand()`.

## Changelog

### 0.4.0 (2026-03-16)

**14 new tools + expanded DNS types.** Full CRUD coverage for all managed resources.

New tools:

- **DNS Zone:** `isp_dns_zone_get`, `isp_dns_zone_update` (SOA NS, TTL, refresh, etc.)
- **Mail:** `isp_mail_domain_update`, `isp_mail_user_update`, `isp_mail_alias_update`, `isp_mail_forward_update`
- **Database:** `isp_db_get`, `isp_db_update`, `isp_db_user_get`, `isp_db_user_update`
- **FTP/Shell:** `isp_ftp_user_get`, `isp_ftp_user_update`, `isp_shell_user_get`, `isp_shell_user_update`

DNS record type expansion:

- `isp_dns_record_add`, `isp_dns_record_update`, `isp_dns_record_delete` now support **9 types**: A, AAAA, MX, TXT, CNAME, SRV, CAA, NS, PTR (was 5)

Other changes:

- Extended `KNOWN_METHODS` with 26 additional API methods
- Added validation schemas for all new tools
- Updated `/ispconfig` command to reflect 65 tools
- Updated `dnsMethodForType()` to support SRV, CAA, NS, PTR

**Total: 65 tools** (was 51)

### 0.3.0 (2026-03-15)

**20 new tools** - update, delete, aliases, forwards.

New tools added:

- **Client:** `isp_client_update`, `isp_client_delete`
- **Sites:** `isp_site_update`, `isp_site_delete`
- **Mail:** `isp_mail_domain_delete`, `isp_mail_alias_list`, `isp_mail_alias_add`, `isp_mail_alias_delete`, `isp_mail_forward_list`, `isp_mail_forward_add`, `isp_mail_forward_delete`
- **DNS:** `isp_dns_zone_delete`, `isp_dns_record_update`
- **Database:** `isp_db_delete`, `isp_db_user_delete`
- **FTP/Shell:** `isp_ftp_user_delete`, `isp_shell_user_delete`
- **Cron:** `isp_cron_delete`, `isp_cron_update`

Other changes:

- Extended `dnsMethodForType()` to support `update` action
- Added validation schemas for all new delete/update tools
- Updated KNOWN_METHODS list to include all new API methods
- Updated `/ispconfig` command with full tool list and usage examples
- Removed em dashes from all output strings and comments

**Total: 51 tools (was 31)**

### 0.2.1 (2026-03-15)

**Bug fix:** Resolve `"Cannot read properties of undefined (reading 'properties')"` crash in OpenClaw UI.

- **Added JSON Schema `parameters` to all 31 tool definitions** - previously tools only had `name`, `description`, and `run`, causing the UI to crash when accessing `tool.parameters.properties`
- **Fixed `registerViaApi()` to pass `parameters` through** to `api.registerTool()` - schemas were defined but never forwarded to OpenClaw
- **Changed tool registration from `run` to `execute`** - OpenClaw's plugin API expects `execute(params)`, not `run(params)`
- **Updated `BoundTool` interface** to include optional `parameters` field
- **Updated `ToolDefinition` interface** to include optional `parameters` field

### 0.2.0 (2026-03-07)

- Initial release with 31 tools, `/ispconfig` command, safety guards

## License

MIT
