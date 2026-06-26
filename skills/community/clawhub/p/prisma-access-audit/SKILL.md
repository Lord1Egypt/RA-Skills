---
name: prisma-access-audit
description: >-
  Palo Alto Prisma Access SASE audit — security policy evaluation for mobile
  users and remote networks, GlobalProtect Cloud Service configuration review,
  service connection validation, threat prevention profile assessment, and
  Strata Cloud Manager posture analysis across Prisma Access tenants.
license: Apache-2.0
metadata:
  safety: read-only
  author: network-security-skills-suite
  version: "1.0.0"
  openclaw: '{"emoji":"☁️","safetyTier":"read-only","requires":{"bins":[],"env":["PRISMA_ACCESS_API_KEY"]},"tags":["prisma-access","palo-alto","sase","zero-trust","globalprotect"],"mcpDependencies":[],"egressEndpoints":["*.prismaaccess.com:443","api.sase.paloaltonetworks.com:443"]}'
---

# Palo Alto Prisma Access SASE Audit

Cloud-delivered security posture audit for Palo Alto Prisma Access tenants.
Unlike on-premises PAN-OS firewall audits that inspect a single device, this
skill evaluates the distributed SASE fabric: security policies governing
mobile users and remote network sites, GlobalProtect Cloud Service client
configuration, threat prevention profiles applied across compute locations,
service connection health to on-premises data centers, and decryption
coverage across all traffic flows.

Covers Prisma Access managed through Strata Cloud Manager (SCM) and legacy
Panorama Cloud Services plugin deployments. Reference
`references/api-reference.md` for Strata Cloud Manager API endpoints,
authentication flows, and response structures used throughout this audit.

## When to Use

- Security policy review after SASE migration from on-premises firewalls to Prisma Access
- Mobile user policy gap analysis — verifying GlobalProtect users receive equivalent or stronger protection than on-premises
- Remote network branch security validation — ensuring IKE/IPSec tunnels enforce consistent policy across all sites
- Threat prevention profile coverage audit — confirming antivirus, anti-spyware, vulnerability protection, and WildFire are bound to all allow rules
- Service connection health assessment — validating connectivity and routing between Prisma Access and on-premises data centers
- GlobalProtect client compliance review — checking client versions, HIP enforcement, and always-on VPN configuration
- Strata Cloud Manager configuration drift detection — comparing running state against intended baseline
- Pre-upgrade baseline capture before Prisma Access infrastructure updates or GlobalProtect client rollouts

## Prerequisites

- Prisma Access API credentials — either Strata Cloud Manager OAuth 2.0 client credentials (Service Account with TSG ID) or legacy Panorama Cloud Services plugin API key
- Understanding of mobile user region deployment — which compute locations serve which user populations and the expected geographic coverage
- Knowledge of remote network topology — site names, IKE peer addresses, expected tunnel counts, and bandwidth allocations per branch
- Documented security policy intent — which traffic categories to inspect, which applications to allow/deny, and expected Security Profile Group assignments per policy rule
- GlobalProtect client version requirements — minimum acceptable client version and HIP check thresholds for the organization
- Access to Cortex Data Lake for log correlation — verifying that policy enforcement matches expected behavior in traffic and threat logs

## Procedure

Follow this audit flow sequentially. Each step builds on prior findings.
The procedure moves from tenant-level infrastructure inventory through
policy analysis per traffic type to logging and visibility validation.

### Step 1: Tenant and Infrastructure Inventory

Authenticate to the Strata Cloud Manager API using OAuth 2.0 client
credentials flow. See `references/api-reference.md` for the token endpoint
and required parameters.

Retrieve tenant information and compute location status:

```
GET https://api.sase.paloaltonetworks.com/sse/config/v1/prisma-access-config
Authorization: Bearer <access_token>
```

Record the following:
- **Tenant ID and TSG ID** — confirm you are auditing the correct tenant
- **Compute locations** — list all active regions for mobile users and remote networks
- **License tier** — Prisma Access edition (Business, Business Premium, or Enterprise) determines available features
- **Bandwidth allocation** — total allocated bandwidth and per-region distribution

Enumerate mobile user regions and remote network sites:

```
GET https://api.sase.paloaltonetworks.com/sse/config/v1/mobile-users/regions
GET https://api.sase.paloaltonetworks.com/sse/config/v1/remote-networks
```

[Mobile Users] Count active compute locations and verify geographic coverage
matches the organization's user distribution.

[Remote Networks] List all configured remote network sites, their IKE
gateway addresses, and tunnel status. Flag any site showing tunnel-down state.

### Step 2: Security Policy Audit (Mobile Users)

Retrieve security policies applied to GlobalProtect mobile users:

```
GET https://api.sase.paloaltonetworks.com/sse/config/v1/security-rules
  ?folder=Mobile Users
```

[Mobile Users] Evaluate each rule against these criteria:

- **Overly permissive application:** Rules with `application: any` combined
  with `action: allow` bypass App-ID identification entirely. Flag as Critical.
- **Missing Security Profile Group:** Allow rules without a bound Security
  Profile Group or individual profiles permit traffic without threat
  inspection. Check `profile_setting` on each rule.
- **Source/destination scope:** Rules using `any` for both source and
  destination address — evaluate whether address objects or address groups
  can narrow the scope.
- **Service port usage:** Rules using `service: any` instead of
  `service: application-default` — App-ID enforcement is strongest when
  applications are restricted to their standard ports.
- **Rule ordering:** Verify that deny/drop rules for known-bad categories
  precede broad allow rules. Misordered rules may permit traffic before
  a deny can evaluate.

Calculate the App-ID adoption ratio: count rules using specific App-IDs
versus rules with `application: any`. Mature deployments target >80% named
App-ID usage.

### Step 3: Security Policy Audit (Remote Networks)

Retrieve security policies applied to remote network sites:

```
GET https://api.sase.paloaltonetworks.com/sse/config/v1/security-rules
  ?folder=Remote Networks
```

[Remote Networks] In addition to the rule-level checks in Step 2, evaluate:

- **IKE/IPSec tunnel configuration:** Verify encryption algorithms meet
  organizational standards (AES-256-GCM preferred, minimum AES-256-CBC).
  Check IKE version (IKEv2 required), DH group (minimum Group 14), and
  SA lifetime settings.

```
GET https://api.sase.paloaltonetworks.com/sse/config/v1/ike-gateways
GET https://api.sase.paloaltonetworks.com/sse/config/v1/ipsec-tunnels
```

- **Routing validation:** Check BGP or static route configuration per site.
  For BGP, verify peer ASN, advertised prefixes, and route filters. For
  static routes, confirm next-hop reachability and subnet accuracy.

```
GET https://api.sase.paloaltonetworks.com/sse/config/v1/bgp-routing
```

- **Split-tunnel vs full-tunnel posture:** Determine whether branch traffic
  is fully tunneled through Prisma Access (recommended for consistent
  inspection) or split-tunneled with direct internet breakout. Split-tunnel
  configurations must ensure local breakout traffic still traverses a
  security policy.

- **Bandwidth allocation:** Verify per-site bandwidth allocation matches
  actual usage. Sites consistently exceeding allocation experience packet
  drops or degraded performance.

### Step 4: Threat Prevention Profile Assessment

Retrieve all Security Profile Groups and individual profiles:

```
GET https://api.sase.paloaltonetworks.com/sse/config/v1/security-profile-groups
GET https://api.sase.paloaltonetworks.com/sse/config/v1/anti-spyware-profiles
GET https://api.sase.paloaltonetworks.com/sse/config/v1/vulnerability-protection-profiles
GET https://api.sase.paloaltonetworks.com/sse/config/v1/wildfire-anti-virus-profiles
```

Evaluate each profile type:

- **Antivirus profile:** Verify action is set to `reset-both` or `drop` for
  all decoders (HTTP, SMTP, IMAP, POP3, FTP, SMB). Default profiles using
  `alert` only are insufficient — flag as High finding.
- **Anti-Spyware profile:** Check that DNS sinkhole is enabled, botnet
  domains are blocked, and spyware severity levels critical/high/medium
  are set to `reset-both` or `drop`.
- **Vulnerability Protection profile:** Verify that critical and high
  severity signatures use `reset-both` action. Default profile uses `alert`
  for informational — acceptable. Check for custom exceptions that weaken
  protection.
- **WildFire profile:** Confirm all file types (PE, APK, Mac OS X, ELF,
  PDF, MS Office, JAR, Flash, Linux pkg) are forwarded to WildFire for
  analysis. Verify WildFire verdict actions block malicious and grayware.
- **File Blocking profile:** Validate that high-risk file types (EXE, DLL,
  BAT, SCR, MSI) are blocked on relevant protocols.

[Mobile Users] [Remote Networks] Verify that all allow rules in both
folders reference a Security Profile Group containing the above profiles.
Rules without profile binding pass traffic uninspected.

### Step 5: URL Filtering and DNS Security

Review URL Filtering and DNS Security configurations:

```
GET https://api.sase.paloaltonetworks.com/sse/config/v1/url-filtering-profiles
GET https://api.sase.paloaltonetworks.com/sse/config/v1/dns-security-profiles
```

- **URL Filtering categories:** Verify that high-risk categories (malware,
  phishing, command-and-control, grayware, newly-registered-domain) are set
  to `block`. Check that the Advanced URL Filtering license is active for
  inline ML-based analysis of unknown URLs.
- **Custom URL categories:** Review any custom URL categories for
  appropriateness — overly broad allow-list categories can bypass security.
- **DNS Security:** Confirm DNS Security policy is applied and that
  DNS-layer threat categories (DGA, DNS tunneling, newly seen domains)
  are set to `sinkhole` or `block`.
- **CASB / SaaS Security:** If licensed, verify that SaaS application
  visibility and inline controls are configured. Check for sanctioned vs
  unsanctioned SaaS application policies.

### Step 6: GlobalProtect Client Configuration

[Mobile Users] Review GlobalProtect Cloud Service configuration:

```
GET https://api.sase.paloaltonetworks.com/sse/config/v1/mobile-agent/global-settings
GET https://api.sase.paloaltonetworks.com/sse/config/v1/hip-profiles
GET https://api.sase.paloaltonetworks.com/sse/config/v1/hip-objects
```

Evaluate the following:

- **Client version currency:** Check minimum supported client version
  against the currently deployed versions across the user population.
  Clients older than the current major release minus one are a compliance
  risk. Query Prisma Access Insights for version distribution.
- **Split-tunnel configuration:** Verify whether the GlobalProtect portal
  configuration uses full-tunnel (all traffic through Prisma Access) or
  split-tunnel (specified apps/domains bypass the tunnel). Full-tunnel is
  recommended for consistent security inspection.
- **HIP (Host Information Profile) checks:** Verify that HIP objects check
  for minimum OS patch level, disk encryption status, antivirus presence
  and currency, host firewall state, and certificate validity. HIP profiles
  should enforce compliance gates — non-compliant devices receive restricted
  access.
- **Pre-logon tunnel:** Check whether a pre-logon tunnel is configured for
  machine-level authentication before user login. Required for environments
  needing machine certificate-based access.
- **Always-on VPN enforcement:** Verify that the GlobalProtect configuration
  enforces always-on VPN with no user-disable option. Check for disable-
  override password protection.
- **Authentication method:** Review SAML, certificate, or LDAP/Kerberos
  authentication. SAML with MFA is recommended for mobile users.

### Step 7: Service Connection Validation

[Service Connections] Verify connectivity between Prisma Access and
on-premises data centers:

```
GET https://api.sase.paloaltonetworks.com/sse/config/v1/service-connections
```

Evaluate each service connection:

- **Tunnel status:** Verify IKE/IPSec tunnel is established and has been
  stable (no recent flaps). Check tunnel uptime and last state change.
- **Routing advertisements:** Confirm that on-premises routes are correctly
  advertised to Prisma Access via BGP. Verify that Prisma Access is
  advertising the expected mobile user and remote network subnets back
  to on-premises.
- **Bandwidth allocation:** Check allocated bandwidth versus utilization.
  Service connections nearing capacity cause traffic drops for mobile users
  accessing on-premises resources.
- **QoS configuration:** If QoS is configured, verify traffic classification
  and bandwidth guarantees align with business application priority.
- **Redundancy:** Verify that primary and secondary service connections exist
  for each data center. Single service connections are a single point of
  failure. Check failover behavior — active/passive or active/active.

### Step 8: Decryption Policy Review

Evaluate SSL/TLS decryption coverage across the Prisma Access tenant:

```
GET https://api.sase.paloaltonetworks.com/sse/config/v1/decryption-rules
  ?folder=Mobile Users
GET https://api.sase.paloaltonetworks.com/sse/config/v1/decryption-rules
  ?folder=Remote Networks
```

[Mobile Users] [Remote Networks] Check decryption configuration:

- **Decryption rule coverage:** Identify which traffic flows are decrypted
  (SSL Forward Proxy) and which bypass decryption. Internet-bound traffic
  from all user and branch sources should be decrypted for full threat
  inspection.
- **Decryption exclusions:** Review technical exclusions (certificate
  pinning, client certificate mutual TLS) and compliance exclusions
  (financial, healthcare categories). Verify exclusion lists are minimal
  and documented with justification.
- **Certificate chain:** Validate that the forward trust CA certificate is
  properly distributed to all endpoints. Mobile user devices must trust the
  decryption CA to avoid certificate errors. Check certificate expiration.
- **TLS version enforcement:** Verify that TLS 1.0 and 1.1 are blocked or
  decrypted with alerts. Only TLS 1.2 and 1.3 should be permitted without
  findings.
- **Performance impact:** For remote network sites with limited bandwidth,
  assess whether decryption processing introduces latency. Check Prisma
  Access Insights for decryption-related performance metrics.

### Step 9: Logging and Visibility

Verify log forwarding and monitoring configuration:

```
GET https://api.sase.paloaltonetworks.com/sse/config/v1/log-forwarding-profiles
```

- **Cortex Data Lake forwarding:** Confirm that all log types (traffic,
  threat, URL, data, WildFire, authentication, HIP match, decryption) are
  forwarded to Cortex Data Lake. Missing log types create visibility gaps.
- **Log retention:** Verify Cortex Data Lake storage allocation and
  retention periods meet compliance requirements. Check for capacity
  warnings.
- **Autonomous DEM (Digital Experience Monitoring):** If licensed, verify
  that Autonomous DEM is enabled for mobile users. Check that application
  performance monitoring targets are configured for critical SaaS
  applications (Microsoft 365, Salesforce, ServiceNow, etc.).
- **External SIEM forwarding:** If logs are forwarded to an external SIEM,
  verify syslog or HTTPS forwarding is functional and that log ingestion
  rates match expected volume.
- **Alert configuration:** Check for configured alerts on critical events —
  tunnel down, license expiration, compute location capacity, high threat
  volume.

## Threshold Tables

### Security Policy Coverage

| Metric | Normal | Warning | Critical |
|--------|--------|---------|----------|
| App-ID adoption (named App-IDs / total allow rules) | >80% | 50-80% | <50% |
| Security Profile Group binding (allow rules with SPG) | >95% | 80-95% | <80% |
| Rules with `application: any` + `service: any` | 0 | 1-3 | >3 |
| Disabled rules in rulebase | <5% of total | 5-15% | >15% |
| Shadowed / unreachable rules | 0 | 1-5 | >5 |

### Threat Prevention Profile Strength

| Profile Type | Normal | Warning | Critical |
|--------------|--------|---------|----------|
| Antivirus — action on all decoders | reset-both / drop | alert on 1-2 decoders | alert-only or default unchanged |
| Anti-Spyware — crit/high severity action | reset-both / drop | drop on critical only | alert-only |
| Anti-Spyware — DNS sinkhole | Enabled | N/A | Disabled |
| Vulnerability Protection — crit/high action | reset-both | drop on critical only | alert-only |
| WildFire — file types forwarded | All file types | Missing 1-2 types | Missing >2 types or disabled |
| File Blocking — high-risk file types | Blocked (EXE/DLL/BAT/SCR) | Partial coverage | Not configured |
| URL Filtering — high-risk categories | Block (malware/phishing/C2) | Alert on some categories | Allow or not configured |
| DNS Security — threat categories | Sinkhole / block | Alert on some | Not configured |

### GlobalProtect Client Compliance

| Metric | Normal | Warning | Critical |
|--------|--------|---------|----------|
| Client version currency (within N-1 major) | >95% compliant | 80-95% compliant | <80% compliant |
| HIP compliance rate (devices passing HIP checks) | >90% | 70-90% | <70% |
| Always-on VPN enforcement | Enabled, no override | Enabled with override password | Disabled |
| Pre-logon tunnel (if required) | Configured and active | Configured, intermittent | Not configured |
| Authentication method | SAML with MFA | SAML without MFA | LDAP/password only |

### Service Connection Health

| Metric | Normal | Warning | Critical |
|--------|--------|---------|----------|
| Tunnel status | Up, stable >7d | Flapping (>2 state changes/24h) | Down |
| Bandwidth utilization | <70% allocated | 70-90% allocated | >90% allocated |
| Redundancy | Primary + secondary active | Single connection, backup configured | Single connection, no backup |
| BGP peer state | Established, routes exchanged | Established, missing routes | Down / not configured |
| Route advertisement accuracy | All expected prefixes present | Missing non-critical prefixes | Missing critical prefixes |

### Decryption Coverage

| Metric | Normal | Warning | Critical |
|--------|--------|---------|----------|
| Internet-bound traffic decrypted | >80% of sessions | 50-80% of sessions | <50% of sessions |
| Decryption exclusion count | <20 categories/domains | 20-50 | >50 |
| TLS 1.0/1.1 traffic | Blocked | Decrypted with alert | Permitted without inspection |
| Forward trust CA certificate validity | >90 days to expiry | 30-90 days | <30 days or expired |

## Decision Trees

### Mobile User Policy Gap Prioritization

```
Mobile User allow rule identified
├── Has Security Profile Group?
│   ├── No → HIGH: Add SPG immediately
│   │   └── Traffic type?
│   │       ├── Internet-bound → Bind full SPG (AV+AS+VP+URL+WF+FB)
│   │       ├── Access to on-prem via service connection → Standard SPG (AV+AS+VP)
│   │       └── SaaS direct access → Full SPG + URL Filtering + CASB
│   └── Yes → Check SPG completeness
│       ├── Missing WildFire → Medium: Add WF profile for zero-day coverage
│       ├── Missing URL Filtering → Medium: Add URL for web threat protection
│       └── All profiles present → OK
│
├── Application = any?
│   ├── Yes + Service = any → CRITICAL: Fully open rule
│   │   └── Review Prisma Access Insights traffic logs for actual app usage
│   │       → Replace with specific App-IDs
│   ├── Yes + Service = specific port → HIGH: App-ID bypass on port
│   │   └── Identify applications on that port from traffic logs
│   │       → Replace with named App-IDs + application-default
│   └── Named App-IDs → OK
│
├── Decrypted?
│   ├── No → SPG inspection limited to metadata
│   │   └── Add decryption rule for this traffic flow
│   └── Yes → Full inspection effective
│
└── HIP-enforced?
    ├── No → Evaluate adding HIP profile for device compliance
    └── Yes → Verify HIP checks match organizational policy
```

### Remote Network Security Posture Remediation

```
Remote network site identified
├── Tunnel status?
│   ├── Down → CRITICAL: Restore connectivity
│   │   ├── Check IKE Phase 1 (peer IP, pre-shared key, proposals)
│   │   ├── Check IKE Phase 2 (proxy IDs, encryption mismatch)
│   │   └── Verify on-prem firewall allows IKE/NAT-T (UDP 500/4500)
│   ├── Flapping → HIGH: Investigate stability
│   │   ├── Check DPD (Dead Peer Detection) settings
│   │   ├── Review ISP stability at branch site
│   │   └── Verify SA lifetime alignment between peers
│   └── Stable → Continue to policy audit
│
├── Encryption strength?
│   ├── Below minimum (3DES, DH Group 2/5) → HIGH: Upgrade proposals
│   │   └── Target: AES-256-GCM, IKEv2, DH Group 19/20
│   └── Meets standard → OK
│
├── Routing correct?
│   ├── BGP: Missing expected prefixes → Verify route filters and advertisements
│   ├── Static: Incorrect next-hop → Correct route configuration
│   └── Routes present and accurate → OK
│
├── Split-tunnel or full-tunnel?
│   ├── Split-tunnel without local security → HIGH: Risk of uninspected traffic
│   │   └── Migrate to full-tunnel or add local security stack
│   └── Full-tunnel or split with local inspection → OK
│
└── Bandwidth adequate?
    ├── >90% utilization → WARNING: Upgrade allocation
    ├── 70-90% utilization → Monitor trend
    └── <70% → OK
```

### Threat Prevention Profile Strengthening Path

```
Threat prevention profile audit
├── Using default (best-practice) profiles?
│   ├── Yes → Acceptable baseline
│   │   └── Review for organizational customization needs
│   └── No → Custom profiles exist
│       ├── Weaker than defaults? → FINDING: Strengthen to match or exceed
│       └── Stronger than defaults? → OK, document customizations
│
├── Antivirus profile
│   ├── Any decoder set to alert-only? → HIGH: Change to reset-both
│   └── All decoders reset-both/drop → OK
│
├── Anti-Spyware profile
│   ├── DNS sinkhole disabled? → HIGH: Enable immediately
│   ├── Critical/high severity = alert? → HIGH: Change to reset-both
│   └── Properly configured → OK
│
├── Vulnerability Protection profile
│   ├── Custom exceptions reducing coverage? → Review each exception
│   │   └── Exception still required? → Document justification
│   │       └── No longer needed → Remove exception
│   └── Standard severity actions → OK
│
└── WildFire profile
    ├── File types not forwarded? → Medium: Add missing file types
    ├── Verdict action = alert for malicious? → HIGH: Change to drop
    └── Full coverage, block malicious → OK
```

## Report Template

```
PRISMA ACCESS SASE AUDIT REPORT
=================================
Tenant: [tenant name]
Tenant ID: [tenant ID]
TSG ID: [TSG ID]
Prisma Access Edition: [Business / Business Premium / Enterprise]
Audit Date: [timestamp]
Performed By: [operator/agent]

INFRASTRUCTURE OVERVIEW:
- Compute locations (Mobile Users): [count] — [region list]
- Remote network sites: [count] — [site list]
- Service connections: [count] — [data center list]
- Total bandwidth allocation: [Mbps]
- Strata Cloud Manager version: [version]

MOBILE USER FINDINGS:
- Total security rules (Mobile Users folder): [count]
- Allow rules: [n] | Deny rules: [n] | Drop rules: [n]
- Rules with Security Profile Groups: [n] / [allow count] ([%])
- App-ID adoption: [n]% of allow rules use named App-IDs
- GlobalProtect client compliance: [n]% on current version
- HIP compliance rate: [n]%

  Findings:
  1. [Severity] [Category] — [Description]
     Rule: [rule name]
     Folder: Mobile Users
     Issue: [specific problem]
     Recommendation: [specific remediation]

REMOTE NETWORK FINDINGS:
- Total remote network sites: [count]
- Sites with tunnel up: [n] / [total]
- Sites with full-tunnel posture: [n] / [total]
- Security rules (Remote Networks folder): [count]
- Rules with Security Profile Groups: [n] / [allow count] ([%])

  Findings:
  1. [Severity] [Category] — [Description]
     Site: [site name]
     Issue: [specific problem — tunnel, routing, policy, or encryption]
     Recommendation: [specific remediation]

THREAT PREVENTION ASSESSMENT:
- Security Profile Groups configured: [count]
- Antivirus profiles: [count] — [strength assessment]
- Anti-Spyware profiles: [count] — DNS sinkhole: [enabled/disabled]
- Vulnerability Protection profiles: [count] — [custom exceptions count]
- WildFire profiles: [count] — file types forwarded: [list]
- URL Filtering: Advanced URL Filtering license: [active/inactive]
- DNS Security: [configured/not configured]

  Findings:
  1. [Severity] [Profile Type] — [Description]
     Profile: [profile name]
     Issue: [specific weakness]
     Recommendation: [specific remediation]

DECRYPTION COVERAGE:
- Mobile User decryption rules: [count]
- Remote Network decryption rules: [count]
- Estimated sessions decrypted: [%]
- Decryption exclusions: [count categories/domains]
- Forward trust CA expiry: [date]
- TLS 1.0/1.1 handling: [blocked/allowed/decrypted]

  Findings:
  1. [Severity] — [Description]
     Scope: [Mobile Users / Remote Networks / Both]
     Issue: [specific gap]
     Recommendation: [specific remediation]

SERVICE CONNECTION STATUS:
- Service connections: [count]
- All tunnels up: [yes/no]
- Redundancy: [all redundant / gaps identified]
- Bandwidth utilization: [average %]

  Findings:
  1. [Severity] — [Description]
     Connection: [service connection name]
     Issue: [tunnel, routing, bandwidth, or redundancy]
     Recommendation: [specific remediation]

SEVERITY SUMMARY:
- Critical: [count]
- High: [count]
- Medium: [count]
- Low / Informational: [count]

REMEDIATION ROADMAP:
Phase 1 (Immediate — 0-7 days):
  - [Critical findings requiring immediate action]

Phase 2 (Short-term — 7-30 days):
  - [High findings and quick wins]

Phase 3 (Medium-term — 30-90 days):
  - [Medium findings, profile hardening, App-ID migration]

Phase 4 (Ongoing):
  - [Continuous monitoring, quarterly re-audit, policy lifecycle]

NEXT AUDIT: [based on findings — CRITICAL: 30d, HIGH: 90d, clean: 180d]
```

## Troubleshooting

### API Authentication — Strata Cloud Manager vs Legacy

Strata Cloud Manager uses OAuth 2.0 client credentials flow. Authenticate
with a Service Account bound to a Tenant Service Group (TSG) ID. The token
endpoint is `https://auth.apps.paloaltonetworks.com/oauth2/access_token`.
Common authentication failures:

- **Invalid TSG ID:** The `scope` parameter must include `tsg_id:<your_tsg_id>`.
  Omitting this or using an incorrect TSG ID returns a 401 error.
- **Expired client secret:** Service Account secrets have configurable
  expiration. Regenerate via Strata Cloud Manager > Identity & Access.
- **Insufficient role:** The Service Account must have at minimum the
  `Auditor` or `View-Only Administrator` role to read configuration.

Legacy Panorama Cloud Services plugin API uses an API key generated from
Panorama. If the organization has migrated to Strata Cloud Manager, the
legacy API may return stale configuration. Always confirm which management
plane is authoritative.

### Compute Location Capacity

Prisma Access compute locations can reach capacity during peak usage. If
mobile user connections are refused or performance degrades:

- Check compute location utilization via Prisma Access Insights or the
  Autonomous DEM dashboard.
- Verify that mobile user regions are distributed geographically to
  balance load — avoid funneling all users through a single region.
- Review bandwidth allocation per compute location. Insufficient allocation
  triggers throttling before true capacity is reached.

### GlobalProtect Client Compatibility

GlobalProtect client compatibility issues commonly arise from:

- **Version mismatch:** Cloud-delivered GlobalProtect infrastructure updates
  independently from client software. Clients more than two major versions
  behind may fail to connect or lose feature support. Check the Prisma
  Access compatibility matrix.
- **OS-specific issues:** macOS system extension requirements (Network
  Extension vs Kernel Extension) change across OS versions. Windows clients
  may conflict with third-party VPN or endpoint security software.
- **MDM-deployed configuration:** Mobile Device Management-pushed profiles
  may override portal-delivered settings. Verify MDM configuration aligns
  with portal/gateway settings.

### Service Connection BGP Flapping

BGP session instability on service connections typically results from:

- **Hold timer mismatch:** Prisma Access uses a default BGP hold time of
  90 seconds. If the on-premises peer uses a shorter hold time and
  keepalives are lost due to congestion, the session drops. Align timers.
- **Route oscillation:** If the on-premises router advertises and withdraws
  routes rapidly, Prisma Access BGP will follow. Check on-premises routing
  stability first.
- **MTU issues:** Path MTU mismatches cause TCP session failures that can
  affect BGP. Verify MTU along the service connection path — typical IPSec
  overhead requires reducing MTU to 1400 or lower.
- **IKE DPD sensitivity:** Aggressive Dead Peer Detection settings combined
  with transient packet loss cause unnecessary tunnel rebuilds. Use a DPD
  interval of 10 seconds with a retry of 3 as a baseline.

### Decryption Certificate Distribution

SSL Forward Proxy decryption requires endpoints to trust the Prisma Access
forward trust CA certificate. Distribution challenges include:

- **Mobile users:** Push the CA certificate via MDM, GPO, or GlobalProtect
  client configuration. Verify distribution by checking certificate store
  on sample devices.
- **Remote network endpoints:** Branch devices behind remote network tunnels
  must also trust the CA. If branch users access the internet via Prisma
  Access, their devices need the certificate.
- **Certificate expiration:** Monitor forward trust CA certificate expiration.
  Prisma Access generates certificates with configurable lifetimes — set
  calendar reminders for renewal. An expired CA causes all decrypted
  sessions to fail with certificate errors.
- **Certificate pinning applications:** Applications that pin their server
  certificates (banking apps, certain healthcare portals) will fail through
  SSL Forward Proxy. Add these to the decryption exclusion list with
  documented justification.
