# ISPConfig Plugin v1.0.0 Roadmap

**Goal:** Full coverage of all 313 ISPConfig Remote API methods.
**Current:** v0.4.1 with 81/309 methods implemented (excluding internal: login/logout/get_function_list/__construct)

---

## Test Strategy

All tests run against the live ISPConfig server (`isp.elvatis.com`).
To protect existing production data:

- **Test prefix:** All test resources use `_test_` prefix (clients, domains, users, etc.)
- **Test domain:** `_test_akido.example` (non-resolvable, safe)
- **Test client:** `_test_akido_client` (created at test start, deleted at end)
- **Cleanup:** Each phase's integration test has a teardown that deletes ALL `_test_` resources
- **Read-only tests:** For list/get operations on existing data, use read-only assertions (no mutations)
- **Credentials:** From `~/.openclaw/.env` (ISP_API_URL, ISP_USER, ISP_PASS)

### Integration Test Pattern
```typescript
describe('Phase X: Category', () => {
  let testClientId: number;
  
  beforeAll(async () => {
    // Create isolated test client
    testClientId = await client.call('client_add', { ... });
  });
  
  afterAll(async () => {
    // Cleanup: delete everything with _test_ prefix
    await client.call('client_delete', { client_id: testClientId });
  });
  
  it('should create/read/update/delete resource', async () => {
    // CRUD cycle within the test client
  });
});
```

---

## Phases

### Phase 1: Core Completion (32 methods)
**Status:** 🔲 Not started

#### Clients (14 new)
- [ ] `client_get_id` — Get client ID by username
- [ ] `client_get_emailcontact` — Get client email
- [ ] `client_get_groupid` — Get client group ID
- [ ] `client_get_by_username` — Lookup client by username
- [ ] `client_get_by_customer_no` — Lookup by customer number
- [ ] `client_get_by_groupid` — Lookup by group ID
- [ ] `client_get_sites_by_user` — List sites for a client
- [ ] `client_change_password` — Change client password
- [ ] `client_delete_everything` — Delete client + all resources
- [ ] `client_login_get` — Get client login data
- [ ] `client_template_additional_get` — Get additional templates
- [ ] `client_template_additional_add` — Add additional template
- [ ] `client_template_additional_delete` — Delete additional template
- [ ] `client_templates_get_all` — List all client templates

#### Server (10 new)
- [ ] `server_get_app_version` — ISPConfig version
- [ ] `server_get_functions` — Available server functions
- [ ] `server_get_php_versions` — List PHP versions
- [ ] `server_get_serverid_by_ip` — Lookup server by IP
- [ ] `server_get_serverid_by_name` — Lookup server by name
- [ ] `server_ip_get` — Get server IP details
- [ ] `server_ip_add` — Add server IP
- [ ] `server_ip_update` — Update server IP
- [ ] `server_ip_delete` — Delete server IP
- [ ] `server_config_set` — Update server config

#### Web Domains (3 new)
- [ ] `sites_web_domain_backup` — Trigger site backup
- [ ] `sites_web_domain_backup_list` — List site backups
- [ ] `sites_web_domain_set_status` — Enable/disable site

#### Quota & Traffic (4 new)
- [ ] `quota_get_by_user` — Disk quota per user
- [ ] `trafficquota_get_by_user` — Traffic quota per user
- [ ] `ftptrafficquota_data` — FTP traffic data
- [ ] `databasequota_get_by_user` — DB quota per user

#### Monitoring (1 new)
- [ ] `monitor_jobqueue_count` — Pending jobs count

---

### Phase 2: DNS Complete (45 methods)
**Status:** 🔲 Not started

#### DNS Record Gets (11 new)
- [ ] `dns_a_get`, `dns_aaaa_get`, `dns_caa_get`, `dns_cname_get`
- [ ] `dns_mx_get`, `dns_ns_get`, `dns_ptr_get`, `dns_srv_get`, `dns_txt_get`
- [ ] `dns_alias_get` (+ add/update/delete = 4)

#### Additional DNS Record Types (28 new)
- [ ] DNAME: get/add/update/delete (4)
- [ ] DS: get/add/update/delete (4)
- [ ] HINFO: get/add/update/delete (4)
- [ ] LOC: get/add/update/delete (4)
- [ ] NAPTR: get/add/update/delete (4)
- [ ] RP: get/add/update/delete (4)
- [ ] SSHFP: get/add/update/delete (4)
- [ ] TLSA: get/add/update/delete (4)

#### DNS Zones Extended (6 new)
- [ ] `dns_slave_get/add/update/delete` (4)
- [ ] `dns_templatezone_add`, `dns_templatezone_get_all`
- [ ] `dns_zone_get_id`
- [ ] `dns_zone_set_status`
- [ ] `dns_zone_set_dnssec`

---

### Phase 3: Mail Complete (~55 methods)
**Status:** 🔲 Not started

- Mail Alias Domains: get/add/update/delete (4)
- Mail Catchall: get/add/update/delete (4)
- Mailing Lists: get/add/update/delete (4)
- Mail User Filters: get/add/update/delete (4)
- Mail User Backup: list/backup (2)
- Mail User by Client: get_all_by_client (1)
- Mail Domain extras: get_by_domain, set_status (2)
- Mail Quota: mailquota_get_by_user (1)
- Fetchmail: get/add/update/delete (4)
- Mail Transport: get/add/update/delete (4)
- Mail Relay Recipient: get/add/update/delete (4)
- Mail Relay Domain: get/add/update/delete (4)
- Spam Filter Whitelist: get/add/update/delete (4)
- Spam Filter Blacklist: get/add/update/delete (4)
- Spam Filter User: get/add/update/delete (4)
- Mail Policy: get/add/update/delete (4)
- Mail Whitelist: get/add/update/delete (4)
- Mail Blacklist: get/add/update/delete (4)
- Mail Filter: get/add/update/delete (4)

---

### Phase 4: Web Extended (~29 methods)
**Status:** 🔲 Not started

- VHost Alias Domains: get/add/update/delete (4)
- VHost Subdomains: get/add/update/delete (4)
- Web Alias Domains: get/add/update/delete (4)
- Web Subdomains: get/add/update/delete (4)
- Web Folders: get/add/update/delete (4)
- Web Folder Users: get/add/update/delete (4)
- WebDAV Users: get/add/update/delete (4)
- FTP: sites_ftp_user_server_get (1)

---

### Phase 5: System & Advanced (~22 methods)
**Status:** 🔲 Not started

- System Config: get/set (2)
- Config Values: get/add/update/replace/delete (5)
- System Datalog: get, get_by_tstamp (2)
- APS Packages: 10 methods
- Domain Registry: get/add/update/delete + list (5)
- Permissions: update_record_permissions (1)

---

### Phase 6: OpenVZ Legacy (22 methods)
**Status:** 🔲 Not started

- OS Templates: get/add/update/delete (4)
- VM Templates: get/add/update/delete (4)
- IPs: get/free/add/update/delete (5)
- VMs: get/get_by_client/add/add_from_template/update/delete/start/stop/restart (9)

---

## Release Plan

After all phases complete:
1. Bump to v1.0.0
2. Full test run (unit + integration)
3. Update README.md, SKILL.md, CHANGELOG.md
4. Publish: GitHub Release → npm → ClawHub
