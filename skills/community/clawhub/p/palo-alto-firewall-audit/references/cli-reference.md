# PAN-OS CLI and API Reference — Audit Commands

Read-only commands organized by audit category for PAN-OS firewall security
policy assessment. All commands are non-modifying (`show`, `test`, `debug`
with read-only flags). Validated against PAN-OS 10.1+ and 11.x.

Three access methods are available:
- **CLI:** SSH to management interface, read-only admin role sufficient
- **XML API:** HTTPS to management interface, API key with read-only admin role
- **REST API:** PAN-OS 9.1+ only, HTTPS with API key, `/restapi/v10.x/` endpoint

## Zone and Interface Inventory

| Function | CLI Command |
|----------|-------------|
| List all zones | `show running zone` |
| Zone detail (interfaces, protection profile) | `show running zone` |
| Zone protection profiles | `show running zone-protection-profile` |
| Interface assignments | `show running interface` |
| Interface status | `show interface all` |
| Interface counters | `show interface <name> counters` |
| VLAN assignments | `show running vlan` |
| Virtual router config | `show running virtual-router` |
| Routing table | `show routing route` |

### Zone Inventory Notes

- `show running zone` displays the committed (running) zone configuration including interface assignments and zone protection profile bindings.
- Compare `show running zone` with `show config merged` output to verify no pending candidate changes affect zone assignments.
- Zone protection profiles are per-zone — a missing binding means no zone-level flood or recon protection for that zone's ingress.

## Security Policy

| Function | CLI Command |
|----------|-------------|
| Full running security policy | `show running security-policy` |
| Security policy (candidate config) | `show config merged running-config security` |
| Policy hit counts | `show rule-hit-count vsys vsys1 security rules all` |
| Test policy match | `test security-policy-match source <IP> destination <IP> protocol <num> application <app> destination-port <port> from <zone> to <zone>` |
| NAT policy | `show running nat-policy` |
| Policy-based forwarding | `show running pbf-policy` |
| Decryption policy | `show running ssl-decryption-policy` |
| DoS protection policy | `show running dos-policy` |
| QoS policy | `show running qos-policy` |

### Security Policy Notes

- `show running security-policy` shows the effective merged rulebase on the firewall, including Panorama pre/post-rules and local rules. This is the authoritative view for audit.
- `show rule-hit-count` reveals rules with zero hits — candidates for cleanup or investigation.
- `test security-policy-match` is the definitive tool for validating which rule matches specific traffic. Always test both the initial L4 match and the expected App-ID to account for app shifts.

### XML API Equivalent

```
GET /api/?type=config&action=get&xpath=/config/devices/entry/vsys/entry[@name='vsys1']/rulebase/security
```

Returns the full security rulebase as XML, suitable for programmatic analysis of large rulebases.

## App-ID Status

| Function | CLI Command |
|----------|-------------|
| App-ID signature version | `show system info | match app-version` |
| App-ID release date | `show system info | match app-release-date` |
| Threat content version | `show system info | match threat-version` |
| Application details | `show running application <app-name>` |
| Application group members | `show running application-group <group-name>` |
| Custom applications | `show running application` (filter for custom) |
| Application filter details | `show running application-filter <filter-name>` |

### App-ID Notes

- `app-version` and `threat-version` in `show system info` indicate content currency. Both should be updated at least weekly; daily is best practice.
- Custom applications override built-in App-ID signatures. Audit custom applications to ensure they do not inadvertently broaden matching.

## Security Profiles

| Function | CLI Command |
|----------|-------------|
| Profile groups | `show running profile-group` |
| Antivirus profiles | `show running virus` |
| Anti-Spyware profiles | `show running spyware` |
| Vulnerability Protection profiles | `show running vulnerability` |
| URL Filtering profiles | `show running url-filtering` |
| File Blocking profiles | `show running file-blocking` |
| WildFire Analysis profiles | `show running wildfire-analysis` |
| Data Filtering profiles | `show running data-filtering` |
| DNS Security config | `show running anti-spyware` (DNS Security section) |

### Security Profile Notes

- `show running profile-group` lists all defined groups and their component profiles. Cross-reference with security policy rules to find rules that reference a profile group vs rules with no profile-setting.
- The "default" profiles (e.g., `default` antivirus profile) ship with PAN-OS but may not provide adequate protection. Audit whether custom profiles with stricter actions have been created and assigned.

## Zone Protection

| Function | CLI Command |
|----------|-------------|
| Zone protection profiles (all) | `show running zone-protection-profile` |
| Active zone protection counters | `show zone-protection zone <zone-name>` |
| DoS protection counters | `show dos-protection rule all` |
| Flood protection statistics | `show counter global filter category flow` |
| Packet buffer utilization | `show running resource-monitor` |

### Zone Protection Notes

- `show zone-protection zone <name>` displays real-time counters for flood detection, recon protection, and packet-based attack protection on the specified zone. Non-zero drop counters indicate active protection.
- Flood protection thresholds (activate, alarm, maximum) should be tuned per zone based on expected traffic volume. Default thresholds may be too high for low-traffic zones or too low for high-traffic zones.

## Decryption

| Function | CLI Command |
|----------|-------------|
| Decryption policy | `show running ssl-decryption-policy` |
| Decryption profiles | `show running decryption-profile` |
| Certificate status | `show sslmgr-store certificate-info` |
| Decryption statistics | `show counter global filter category ssl` |
| Decrypted session count | `show session all filter ssl-decrypt yes` |
| Decryption exclusions | `show running ssl-decryption-exclude-list` |
| Certificate chain issues | `show sslmgr-store certificate-cache` |

### Decryption Notes

- `show session all filter ssl-decrypt yes` reveals the volume of currently decrypted sessions. Compare against total session count for a decryption coverage ratio.
- Certificate warnings in `show sslmgr-store certificate-info` (expired, untrusted chain) will cause client-side errors. Audit certificate validity before and after enabling decryption.

## Session and Traffic

| Function | CLI Command |
|----------|-------------|
| Active session summary | `show session info` |
| Session table (filtered) | `show session all filter source <IP> destination <IP> application <app>` |
| Session by rule | `show session all filter rule <rule-name>` |
| Session by zone | `show session all filter from <zone> to <zone>` |
| Traffic logs (recent) | `show log traffic direction equal 1 receive_time in last-hour` |
| Threat logs (recent) | `show log threat direction equal 1 receive_time in last-hour` |
| URL logs (recent) | `show log url receive_time in last-hour` |
| ACC (Application Command Center) | Web UI: Monitor → ACC (no CLI equivalent) |

### Session and Traffic Notes

- `show session info` provides total active sessions, session setup rate, and TCP/UDP/ICMP breakdown. Use this for baseline capacity assessment.
- Traffic logs filtered by rule name help identify which rules carry the most traffic — prioritize audit effort on high-volume rules.
- The ACC (Application Command Center) in the web UI is the best tool for visualizing application mix, threat activity, and blocked categories. It has no direct CLI equivalent but the data can be queried via XML API log queries.

## System Status

| Function | CLI Command |
|----------|-------------|
| System info (version, uptime, serial) | `show system info` |
| HA status | `show high-availability all` |
| Management plane resources | `show system resources` |
| Data plane resources | `show running resource-monitor` |
| License status | `show system license` |
| Software version | `show system info | match sw-version` |
| Content update schedule | `show system info | match content` |
| Job history (updates, commits) | `show jobs processed` |
| Panorama connection status | `show panorama-status` |
| GlobalProtect status | `show global-protect-gateway current-user` |

### System Status Notes

- `show system info` is the single most important baseline command — it provides PAN-OS version, App-ID version, threat version, uptime, serial number, and model.
- `show high-availability all` reveals HA state (active/passive, active/active), sync status, and failover history. Audit findings should be validated on both HA members.
- `show panorama-status` confirms whether the firewall is currently connected to Panorama. A disconnected firewall may have stale pre/post-rules.

## XML API Query Examples

For programmatic audit of large environments, the XML API is preferred over CLI scraping.

| Function | API Call |
|----------|---------|
| Full security rulebase | `GET /api/?type=config&action=get&xpath=/config/devices/entry/vsys/entry[@name='vsys1']/rulebase/security` |
| Security profiles | `GET /api/?type=config&action=get&xpath=/config/devices/entry/vsys/entry[@name='vsys1']/profiles` |
| Zone configuration | `GET /api/?type=config&action=get&xpath=/config/devices/entry/vsys/entry[@name='vsys1']/zone` |
| Operational command (session info) | `GET /api/?type=op&cmd=<show><session><info></info></session></show>` |
| Traffic log query | `GET /api/?type=log&log-type=traffic&query=(rule eq 'rulename')&nlogs=100` |
| System info | `GET /api/?type=op&cmd=<show><system><info></info></system></show>` |

### API Notes

- XML API uses API key authentication: `GET /api/?type=keygen&user=<user>&password=<pass>` to generate a key, then pass `&key=<apikey>` on subsequent requests.
- REST API (PAN-OS 9.1+) provides a more modern interface at `/restapi/v10.x/` with JSON responses. Supports the same read-only operations.
- For audit purposes, create a dedicated API-only admin account with the read-only admin role. This ensures audit tooling cannot modify configuration.
