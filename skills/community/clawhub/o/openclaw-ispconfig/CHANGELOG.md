# Changelog

## 1.0.0 (2026-03-17)

**Full ISPConfig API coverage: 292 tools.**

### Added
- **Phase 1 (Core):** 32 new tools for Clients (lookups, templates, password), Server (PHP versions, IPs, app version), Web Domain backups/status, Quota/Traffic, Monitoring
- **Phase 2 (DNS):** 54 new tools for all DNS record types (DNAME, DS, HINFO, LOC, NAPTR, RP, SSHFP, TLSA, ALIAS), individual record gets, DNS slaves, template zones, DNSSEC
- **Phase 3 (Mail):** 66 new tools for alias domains, catchall, mailing lists, user filters, fetchmail, transport, relay, spam filters, policies, blacklist/whitelist
- **Phase 4 (Web Extended):** 29 new tools for VHost alias domains, VHost subdomains, web alias domains, web subdomains, web folders, folder users, WebDAV users
- **Phase 5 (System):** 25 new tools for system config, config values, datalog, APS packages, domain registry, permissions
- **Phase 6 (OpenVZ):** 22 new tools for OS templates, VM templates, IPs, VMs (full lifecycle)

### Changed
- `dnsMethodForType` now supports all DNS record types (was: A/AAAA/MX/TXT/CNAME/SRV/CAA/NS/PTR)
- Updated test assertions for expanded DNS type support

## 0.4.1 (2026-03-15)

- Bug fixes: missing schemas, parameters pass-through, run vs execute
- 64 tools (15 read + 14 write + 1 alias + 1 provisioning + extras)

## 0.2.1 (2026-03-15)

- Initial release with core CRUD operations
- 31 tools for clients, sites, DNS, mail, databases, FTP, shell, cron
