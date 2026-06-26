---
name: palo-alto-firewall-audit
description: >-
  PAN-OS zone-based security policy audit with App-ID/Content-ID analysis,
  Security Profile Group validation, zone protection assessment, and decryption
  policy review. Systematic rule-by-rule evaluation for Palo Alto Networks
  PA-series and VM-series firewalls.
license: Apache-2.0
metadata:
  safety: read-only
  author: network-security-skills-suite
  version: "1.0.0"
  openclaw: '{"emoji":"🛡️","safetyTier":"read-only","requires":{"bins":[],"env":["PAN_API_KEY"]},"tags":["palo-alto","firewall","audit","security"],"mcpDependencies":["palo-alto-mcp"],"egressEndpoints":["*.paloaltonetworks.com:443"]}'
---

# PAN-OS Firewall Security Policy Audit

Policy-audit-driven analysis of Palo Alto Networks PAN-OS security policies.
Unlike generic firewall checklists that check for open ports and default-deny,
this skill evaluates the PAN-OS-specific security architecture: zone-based
segmentation, the App-ID identification chain, Security Profile Group binding
coverage, and policy evaluation order.

Covers PAN-OS 10.x+ on PA-series hardware and VM-series virtual firewalls.
For Panorama-managed deployments, the audit addresses device group hierarchy
and pre/post-rule evaluation. Reference `references/policy-model.md` for the
full packet evaluation chain and `references/cli-reference.md` for read-only
CLI and API commands.

## When to Use

- Security policy review after rule changes or migration from port-based rules
- Annual or quarterly compliance audit requiring rule-level justification
- Post-incident rule assessment to identify how traffic was permitted
- Zone segmentation validation after network redesign or VLAN changes
- Security Profile Group gap analysis — finding allow rules without threat inspection
- App-ID adoption assessment — measuring migration from `application any` to named App-IDs
- Pre-upgrade policy baseline before PAN-OS major version upgrades
- Panorama push validation — confirming device group rules are consistent across managed firewalls

## Prerequisites

- Read-only administrative access to PAN-OS CLI, XML API, or REST API (PAN-OS 9.1+ for REST)
- Understanding of the zone topology — which zones exist, their trust classification, and expected traffic flows between zone pairs
- Knowledge of expected application allowlists per zone pair (which App-IDs should be permitted where)
- Awareness of Security Profile Group assignments — which profile group should apply to which traffic categories
- For Panorama-managed environments: access to Panorama with visibility into device group hierarchy
- Candidate configuration committed — audit evaluates the running configuration, not candidate

## Procedure

Follow this audit flow sequentially. Each step builds on prior findings.
The procedure moves from architecture inventory through rule-level analysis
to profile and protection validation.

### Step 1: Zone Architecture Inventory

Collect all security zones and their assignments.

```
show running zone
```

Record each zone: name, type (L3/L2/V-Wire/Tap/Tunnel), assigned interfaces,
and zone protection profile. Count inter-zone security policy rules per zone
pair. Identify zones with no protection profile assigned — these lack flood,
reconnaissance, and packet-based attack protection.

Check the zone protection profile configuration for each active zone:

```
show running zone-protection-profile
```

Flag any L3 zone without a zone protection profile as a finding.

### Step 2: Security Policy Rule-by-Rule Analysis

Retrieve the full security rulebase:

```
show running security-policy
```

For Panorama-managed devices, rules evaluate in this order: pre-rules →
local rules → post-rules. Evaluate each rule against these criteria:

- **Overly permissive application:** Rules with `application any` combined
  with `action allow` are Critical findings — they bypass App-ID entirely,
  permitting any application matching the zone/IP/port tuple.
- **Missing Security Profile Group:** Allow rules without a Security Profile
  Group (or individual profiles) pass traffic without threat inspection.
  Check `profile-setting` on each allow rule.
- **Disabled rules:** Rules with `disabled yes` still consume rulebase space
  and create audit confusion. Flag for cleanup.
- **Shadowed rules:** A rule is shadowed when a preceding rule matches all
  the same traffic with equal or broader criteria. Shadowed rules never match.
  Compare source/destination zone, address, application, and service fields.
- **Overly broad source/destination:** Rules using `any` for both source and
  destination address within a zone pair — evaluate whether address objects
  can narrow the scope.

Use `test security-policy-match` to validate specific traffic scenarios:

```
test security-policy-match source <IP> destination <IP> protocol <num> application <app> destination-port <port> from <zone> to <zone>
```

### Step 3: App-ID Coverage Assessment

Quantify App-ID adoption across the rulebase.

Count rules using `application any` versus rules with specific App-IDs.
Calculate the ratio — mature deployments target >80% of allow rules using
named App-IDs rather than `application any`.

Verify App-ID signature currency:

```
show system info
```

Check `app-version` and `app-release-date`. Signatures older than 7 days
indicate update failures. App-ID accuracy depends on current signatures.

For rules still using `application any`, check if they also restrict by
`service` (port/protocol). Rules with `application any` + `service any` are
the highest-risk combination — they permit all applications on all ports.

### Step 4: Security Profile Group Validation

Verify threat inspection coverage on traffic-allowing rules.

```
show running profile-group
```

A complete Security Profile Group includes: Antivirus, Anti-Spyware,
Vulnerability Protection, URL Filtering, File Blocking, and WildFire
Analysis. Optionally, Data Filtering for DLP.

For each allow rule, check `profile-setting`:
- **group** — a Security Profile Group is bound (best practice)
- **profiles** — individual profiles are bound (acceptable, verify completeness)
- **none** — no profiles bound (finding: traffic passes uninspected)

Validate that the profile group used on internet-facing rules includes
WildFire Analysis for zero-day protection. Internal-only rules may use a
lighter profile group, but should still include Anti-Spyware at minimum.

### Step 5: Zone Protection Profile Audit

Evaluate zone-level protections independently from security policy.

Zone Protection Profiles defend against volumetric and packet-based attacks
at the zone ingress point, before security policy evaluation.

Check each zone's protection profile for:
- **Flood protection:** SYN flood (SYN cookies threshold), UDP flood, ICMP
  flood, and Other IP flood — verify activate/alarm/maximum rates are set
  appropriately for the zone's expected traffic volume
- **Reconnaissance protection:** TCP/UDP port scan detection and host sweep
  detection — should be enabled on external-facing zones
- **Packet-based attack protection:** IP spoofing, fragmented traffic,
  known-bad flags (SYN+FIN, NULL flags), strict IP address check

### Step 6: Decryption Policy Review

Evaluate SSL/TLS decryption coverage.

```
show running ssl-decryption-policy
```

Without decryption, Security Profiles cannot inspect encrypted traffic —
threat inspection is limited to connection metadata. Check:

- **Decryption rule coverage:** Which zone pairs have SSL Forward Proxy
  decryption enabled? Internet-bound traffic from user zones should be
  decrypted for full threat inspection.
- **Certificate status:** Forward trust/untrust CA certificate validity and
  distribution to endpoints.
- **Exclusions:** Technical and compliance exclusions (financial, healthcare
  categories). Verify exclusion lists are minimal and justified.
- **SSH decryption:** Inbound SSH proxy rules for server segments, if applicable.

## Threshold Tables

### Policy Rule Severity Classification

| Finding | Severity | Rationale |
|---------|----------|-----------|
| `application any` + `action allow` + `service any` | Critical | Permits all applications on all ports — no App-ID or port restriction |
| `application any` + `action allow` (specific service) | High | Bypasses App-ID on specified ports — permits any application on those ports |
| Allow rule without Security Profile Group | High | Traffic passes without AV, anti-spyware, or vulnerability inspection |
| Allow rule with incomplete profile group (missing WF/URL) | Medium | Partial inspection — zero-day and URL threats uninspected |
| Disabled rule in production rulebase | Medium | Audit confusion; cleanup recommended |
| Shadowed rule (never matches) | Medium | Dead configuration; remove or reorder |
| Zone without zone protection profile | High | No flood, recon, or packet-based attack defense at zone boundary |
| Decryption not enabled on internet-bound traffic | High | Encrypted traffic bypasses content inspection |
| App-ID signatures >7 days old | Medium | Application identification accuracy degraded |
| Rule with `any` source and `any` destination | Medium | Overly broad scope — evaluate address narrowing |

### App-ID Adoption Maturity

| App-ID Rule Ratio | Maturity | Guidance |
|-------------------|----------|----------|
| >80% named App-IDs | Mature | Maintain; review remaining `any` rules quarterly |
| 50–80% named App-IDs | Developing | Prioritize high-traffic `any` rules for App-ID migration |
| <50% named App-IDs | Immature | Systematic App-ID migration needed — begin with known applications |

## Decision Trees

### Overly Permissive Rule Remediation

```
Rule has application = any
├── Also service = any?
│   ├── Yes → CRITICAL: Fully open rule
│   │   ├── Is this a temporary migration rule?
│   │   │   ├── Yes → Set expiration date, add to migration tracker
│   │   │   └── No → Immediate remediation required
│   │   └── Identify actual applications via Traffic Log:
│   │       show log traffic rule equal <rulename>
│   │       → Replace with specific App-IDs + service
│   └── No (specific service)
│       └── HIGH: Port-restricted but App-ID bypassed
│           └── Identify applications on that port via ACC
│               → Replace application any with observed App-IDs
│
├── Security Profile Group bound?
│   ├── No → Add profile group BEFORE narrowing App-ID
│   │   └── Ensures threat visibility during migration
│   └── Yes → Proceed with App-ID migration
│
└── Rule disabled?
    ├── Yes → Schedule removal after change window
    └── No → Active rule, proceed with analysis above
```

### Missing Security Profile Group Remediation

```
Allow rule without profile-setting
├── Traffic type?
│   ├── Internet-bound → Bind full SPG (AV+AS+VP+URL+FB+WF)
│   ├── Inter-zone internal → Bind standard SPG (AV+AS+VP minimum)
│   ├── Intrazone → Evaluate risk; bind AS+VP minimum
│   └── Management traffic → Bind AS+VP; URL/WF optional
│
├── Decrypted traffic?
│   ├── Yes → Full SPG effective; bind complete group
│   └── No → SPG limited to metadata inspection
│       └── Evaluate adding decryption first
│
└── Performance concern?
    ├── Session rate >100K/s → Use hardware-accelerated profiles
    └── Below threshold → Full SPG with default settings
```

## Report Template

```
PAN-OS SECURITY POLICY AUDIT REPORT
=====================================
Device: [hostname]
PAN-OS Version: [version]
Platform: [PA-xxxx / VM-series]
Management: [standalone / Panorama device-group name]
Audit Date: [timestamp]
Performed By: [operator/agent]

ZONE ARCHITECTURE:
- Zones configured: [count]
- Zones with protection profiles: [n] / [total]
- Zone pairs with security policy: [count]

POLICY SUMMARY:
- Total security rules: [count]
- Allow rules: [n] | Deny rules: [n] | Drop rules: [n]
- Rules with Security Profile Groups: [n] / [allow count]
- App-ID adoption: [n]% of allow rules use named App-IDs

FINDINGS:
1. [Severity] [Category] — [Description]
   Rule: [rule name]
   Zone Pair: [from-zone] → [to-zone]
   Issue: [specific problem]
   Current Config: [what the rule does now]
   Recommendation: [specific remediation]

DECRYPTION COVERAGE:
- Zone pairs with SSL Forward Proxy: [list]
- Estimated encrypted traffic inspected: [%]
- Exclusion categories: [count]

APP-ID MATURITY:
- Named App-ID rules: [n] / [total allow] ([%])
- Top application-any rules by hit count: [list top 5]

RECOMMENDATIONS:
- [Prioritized action list by severity]

NEXT AUDIT: [based on findings — CRITICAL findings: 30d, HIGH: 90d, clean: 180d]
```

## Troubleshooting

### Large Rulebases (>500 Rules)

Auditing large rulebases manually is impractical. Use the XML API to export
the full policy as structured data for programmatic analysis:
`/api/?type=config&action=get&xpath=/config/devices/entry/vsys/entry/rulebase/security`
Parse the XML to automate shadow detection, profile coverage gaps, and App-ID
ratio calculations. Prioritize by hit count — rules with zero hits in 90 days
are cleanup candidates.

### Panorama Shared vs Device-Group Policies

In Panorama-managed environments, rules exist at multiple levels: shared
pre-rules → device-group pre-rules → local rules → device-group post-rules
→ shared post-rules. An audit must evaluate the effective rulebase on each
managed firewall, not just the Panorama device group in isolation. Use
`show running security-policy` on individual firewalls to see the merged
effective policy.

### Dynamic Address Groups

Rules referencing dynamic address groups (DAGs) with tag-based membership
complicate audit — the effective scope changes as tagged objects are
added/removed. Check current membership with
`show object dynamic-address-group all` and note that findings may shift
as membership changes. Document the DAG evaluation at audit time.

### GlobalProtect and Captive Portal Zones

Traffic from GlobalProtect VPN users and Captive Portal-authenticated
sessions may enter zones differently than standard interface traffic. Verify
that security policies cover GP tunnel zones and that User-ID integration
is functioning for identity-based rules.

### Content Update Failures

If App-ID or Threat Prevention signatures are outdated, audit findings may
not reflect current threat landscape. Verify update schedules:
`show system info | match content` and `show jobs processed`. Resolve
update failures before finalizing the audit report.
