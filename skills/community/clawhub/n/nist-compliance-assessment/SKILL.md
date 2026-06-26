---
name: nist-compliance-assessment
description: >-
  NIST Cybersecurity Framework (CSF) and SP 800-53 Rev 5 compliance assessment
  for network infrastructure. Maps device configuration against 6 control
  families with direct network device relevance — Access Control (AC), Audit
  and Accountability (AU), Configuration Management (CM), Identification and
  Authentication (IA), System and Communications Protection (SC), and System
  and Information Integrity (SI). Focuses on CSF Protect (PR) and Detect (DE)
  functions for network security posture assessment.
license: Apache-2.0
metadata:
  safety: read-only
  author: network-security-skills-suite
  version: "1.0.0"
  openclaw: '{"emoji":"📋","safetyTier":"read-only","requires":{"bins":["ssh"],"env":[]},"tags":["nist","compliance","800-53"],"mcpDependencies":[],"egressEndpoints":[]}'
---

# NIST CSF and SP 800-53 Compliance Assessment

Compliance assessment skill that maps network device configuration and
operational state against NIST SP 800-53 Rev 5 controls and the NIST
Cybersecurity Framework (CSF) 2.0 functions. Assesses 6 of the 20 NIST
800-53 control families that have direct network device relevance:

- **AC** — Access Control
- **AU** — Audit and Accountability
- **CM** — Configuration Management
- **IA** — Identification and Authentication
- **SC** — System and Communications Protection
- **SI** — System and Information Integrity

The remaining 14 control families (AT, CA, CP, IR, MA, MP, PE, PL, PM, PS,
PT, RA, SA, SR) are outside the scope of network device configuration
assessment — they address organizational processes, physical security,
personnel, supply chain, or system-level concerns not directly observable
in device configuration.

Focuses on CSF **Protect (PR)** and **Detect (DE)** functions, which map
most directly to network device hardening and monitoring controls. NIST
SP 800-53 and the CSF are public-domain US government publications.

Consult `references/control-reference.md` for the full control-to-CSF
mapping table and `references/cli-reference.md` for per-platform read-only
verification commands.

## When to Use

- Federal agency compliance under FISMA — mapping network infrastructure
  controls to NIST 800-53 baselines at Low, Moderate, or High impact levels
- Government contractor assessments requiring NIST 800-171 or CMMC alignment
- Enterprise NIST CSF adoption — structuring network security posture
  assessment around CSF functions (Identify, Protect, Detect, Respond, Recover)
- Security posture baselining — establishing measurable control compliance
  state before and after remediation
- Audit preparation for NIST-referenced frameworks (FedRAMP, CMMC, state and
  local government standards)
- Risk management input — providing control gap evidence for organizational
  risk assessments per NIST RMF

## Prerequisites

- Read-only CLI or API access to target network devices (SSH, console, or
  management API with non-modifying privileges)
- System FIPS 199 security categorization — the impact level (Low, Moderate,
  High) determines which 800-53 controls apply as baseline
- NIST SP 800-53 Rev 5 or CSF 2.0 document for reference (freely available
  from csrc.nist.gov)
- System boundary definition — which devices are within the authorization
  boundary
- Network architecture diagrams showing device roles and trust zones
- Awareness of inherited controls — controls satisfied by the environment
  versus controls the device must implement directly

## Procedure

Follow this seven-step compliance assessment flow. Steps 2–7 each assess
one NIST 800-53 control family. Within each family, the listed controls are
the subset most relevant to network device configuration — the full family
contains additional controls assessed at the system or organizational level.

### Step 1: Assessment Scope and Framework Selection

Define the assessment boundary and select the target framework mapping.

**Framework selection:** Determine whether mapping to CSF functions
(Identify/Protect/Detect/Respond/Recover) or directly to 800-53 control
families. CSF provides a high-level posture view; 800-53 provides
control-level detail required for FISMA compliance.

**Impact level:** Identify the system's FIPS 199 categorization:
- **Low** — limited adverse effect from loss of confidentiality, integrity,
  or availability
- **Moderate** — serious adverse effect
- **High** — severe or catastrophic adverse effect

The impact level determines the control baseline — High-impact systems
require more controls and stricter implementation than Low-impact systems.

**System boundary:** List all network devices within the authorization
boundary. Record hostname, platform, OS version, and device role (boundary,
core, distribution, access, management).

### Step 2: Access Control (AC)

Assess controls governing who and what can access device resources.

**AC-2 Account Management:** Verify local accounts are documented and
authorized. Check for default, shared, or dormant accounts.

**[Cisco]** `show running-config | include username` — list local accounts
and privilege levels.
**[JunOS]** `show configuration system login` — review login classes and
user accounts.
**[EOS]** `show running-config section username` — list local user accounts.
**[PAN-OS]** `show admins all` — list administrative accounts.

**AC-3 Access Enforcement:** Verify role-based access control separates
read-only, operator, and administrative privileges.

**AC-6 Least Privilege:** Confirm accounts operate at the minimum privilege
level required. Flag any non-admin account with privilege level 15 (Cisco)
or superuser class (JunOS).

**AC-12 Session Termination:** Verify idle session timeouts on VTY, console,
and management interfaces.

**[Cisco]** `show running-config | section line` — check `exec-timeout` on
VTY and console lines.
**[JunOS]** `show configuration system login` — check `idle-timeout` value.
**[PAN-OS]** `show config running | match idle-timeout` — verify admin
session timeout.

**AC-17 Remote Access:** Confirm remote management uses encrypted protocols
only (SSH, HTTPS). Verify Telnet and HTTP are disabled. Check source address
restrictions on management access.

**[Cisco]** `show ip ssh` — verify SSH version 2, check `transport input ssh`
on VTY lines.
**[EOS]** `show management ssh` — verify SSH configuration and version.

### Step 3: Audit and Accountability (AU)

Assess controls governing event logging, log protection, and time accuracy.

**AU-2 Audit Events:** Verify logging captures security-relevant events
including login attempts, configuration changes, privilege escalation,
and ACL matches.

**[Cisco]** `show logging` — verify buffer level and remote syslog servers.
**[JunOS]** `show configuration system syslog` — verify log targets and
facility/severity mappings.
**[EOS]** `show logging` — check logging hosts and severity levels.
**[PAN-OS]** `show logging-status` — verify log forwarding to Panorama
or external SIEM.

**AU-3 Content of Audit Records:** Confirm log entries include timestamp,
event type, source, outcome (success/failure), and identity of subject.

**AU-4 Audit Log Storage:** Verify local log buffer capacity and remote
log destination redundancy. Check that log storage does not auto-overwrite
before offload.

**AU-6 Audit Review and Analysis:** Confirm logs are forwarded to a central
analysis platform (SIEM) where correlation and alerting are possible.

**AU-8 Time Stamps:** Verify NTP synchronization with authenticated, trusted
time sources. Timestamps must be accurate for log correlation across devices.

**[Cisco]** `show ntp associations` and `show ntp status` — verify NTP
peers and synchronization state.
**[JunOS]** `show ntp associations` — verify NTP peer reachability and
stratum.
**[PAN-OS]** `show ntp` — verify NTP server configuration and sync status.

### Step 4: Configuration Management (CM)

Assess controls governing configuration integrity and change control.

**CM-2 Baseline Configuration:** Compare running configuration against an
approved baseline. Any drift indicates unauthorized or undocumented changes.

**[Cisco]** `show archive config differences` — diff running vs startup
configuration.
**[JunOS]** `show system rollback compare 0 1` — compare current config
with prior version.
**[EOS]** `show running-config diffs` — review configuration changes.

**CM-3 Configuration Change Control:** Verify configuration archive and
rollback capability. Check whether change history is preserved.

**CM-6 Configuration Settings:** Verify device configuration matches
organizational security configuration checklists. Check for hardened
settings per device role.

**CM-7 Least Functionality:** Confirm unnecessary services are disabled.

**[Cisco]** `show running-config | include ^service|^no service` — verify
disabled services (finger, pad, tcp-small-servers, udp-small-servers,
ip source-route, LLDP/CDP where not needed).
**[JunOS]** `show configuration system services` — verify only required
services (SSH, NetConf) are enabled.
**[EOS]** `show running-config | include management|service` — check for
unnecessary services.
**[PAN-OS]** `show running management-profile` — verify management profiles
expose only required services.

### Step 5: Identification and Authentication (IA)

Assess controls governing identity verification and credential management.

**IA-2 Identification and Authentication (Organizational Users):** Verify
centralized authentication via AAA (TACACS+/RADIUS). Confirm local fallback
accounts exist but are not the primary authentication method.

**[Cisco]** `show running-config | section aaa` — verify `aaa new-model`,
TACACS+/RADIUS server groups, method lists.
**[JunOS]** `show configuration system authentication-order` — verify
TACACS+/RADIUS is first in authentication order.
**[EOS]** `show running-config section aaa` — verify AAA configuration.

**IA-3 Device Identification and Authentication:** Verify device-to-device
authentication for routing protocol peers and management connections.
Check 802.1X on access ports where applicable.

**IA-5 Authenticator Management:** Verify password complexity enforcement,
credential hashing strength, and SSH key management.

**[Cisco]** `show running-config | include username` — verify `secret 9`
(scrypt) or `algorithm-type scrypt` hashing.
**[JunOS]** `show configuration system login password` — check password
requirements.
**[PAN-OS]** `show config running | match password-complexity` — verify
complexity profile exists and is enforced.

Check SNMP credentials — SNMP v3 with authentication and encryption (authPriv)
should replace SNMP v1/v2c community strings.

**[Cisco]** `show snmp user` — verify SNMPv3 users with authPriv security.
**[JunOS]** `show configuration snmp v3` — verify v3 USM configuration.

### Step 6: System and Communications Protection (SC)

Assess controls governing boundary defense and data transmission security.

**SC-7 Boundary Protection:** Verify ACLs enforce traffic filtering at
network boundaries. Check that infrastructure addresses are protected from
data plane access.

**[Cisco]** `show ip access-lists` — review boundary ACLs for explicit deny
and logging.
**[JunOS]** `show configuration firewall family inet` — review filter rules
on boundary interfaces.
**[EOS]** `show ip access-lists` — review ACL configuration.
**[PAN-OS]** `show running security-policy` — review zone-based policies on
boundary zones.

**SC-8 Transmission Confidentiality and Integrity:** Verify management and
control plane traffic uses encryption in transit (SSH, TLS, IPsec, MACsec).
Check that no cleartext protocols (Telnet, HTTP, SNMPv1/v2c) carry
sensitive data.

**SC-10 Network Disconnect:** Verify session timeout on inactive management
connections and VPN tunnels. Dead peer detection on IPsec tunnels should
terminate stale sessions.

**SC-13 Cryptographic Protection:** Audit cryptographic algorithms in use.
Flag deprecated algorithms: DES, 3DES, RC4, MD5 for authentication.
Verify minimum standards (AES-128+, SHA-256+).

**[Cisco]** `show crypto ipsec sa` — check encryption and hash algorithms
on active tunnels.
**[JunOS]** `show security ike security-associations` — review IKE
proposal algorithms.
**[PAN-OS]** `show vpn ipsec-sa` — verify tunnel encryption parameters.

### Step 7: System and Information Integrity (SI)

Assess controls governing flaw remediation, monitoring, and software
integrity.

**SI-2 Flaw Remediation:** Check device OS version against vendor security
advisories. Verify the device is running a version with no known critical
vulnerabilities.

**[Cisco]** `show version` — capture IOS/IOS-XE version for advisory check.
**[JunOS]** `show version` — capture Junos version for CVE review.
**[EOS]** `show version` — capture EOS version.
**[PAN-OS]** `show system info` — capture PAN-OS version and content updates.

**SI-4 System Monitoring:** Verify IDS/IPS, NetFlow, or traffic monitoring
is active on critical segments.

**SI-5 Security Alerts and Advisories:** Confirm subscription to vendor
security advisory channels (Cisco PSIRT, Juniper, Palo Alto, Arista).

**SI-7 Software, Firmware, and Information Integrity:** Verify device image
integrity where supported.

**[Cisco]** `show software authenticity running` — verify image digital
signature (IOS-XE).
**[JunOS]** `show system storage` and `show system license` — verify system
integrity indicators.
**[PAN-OS]** `show system info | match sw-version` — check against known-good
version hash from vendor.

## Threshold Tables

### Control Gap Severity

| Severity | Impact Level | Condition | Examples |
|----------|-------------|-----------|----------|
| Critical | High-impact baseline | Baseline control gap on boundary or critical infrastructure device | AC-2 no account management on internet-facing router, SC-7 no boundary ACLs, IA-2 no authentication on management access |
| High | Moderate-impact baseline | Required baseline control missing or partially implemented | AU-2 no security event logging, IA-2 no MFA for privileged access, SC-8 cleartext management protocols in use |
| Medium | Low-impact baseline | Baseline control gap with limited exposure | CM-7 unnecessary services enabled on internal device, AU-8 NTP not authenticated, AC-12 no idle session timeout |
| Low | Enhancement gap | Control beyond required baseline not implemented | Advanced NetFlow analytics, MACsec on internal links, granular RBAC beyond baseline requirement |

### Compliance Posture by Impact Level

| Score Range | Posture | Guidance |
|-------------|---------|----------|
| 90–100% | Satisfactory | Address residual gaps in next assessment cycle |
| 70–89% | Conditional | Develop POA&M for remaining gaps, prioritize High-impact families |
| 50–69% | Deficient | Immediate remediation plan required, escalate to ISSO/AO |
| <50% | Unsatisfactory | System may not meet authorization threshold, consider risk acceptance or isolation |

## Decision Trees

### Control Gap Remediation Priority

```
Control gap identified
├── What is the system impact level?
│   ├── High
│   │   ├── Is this a baseline control for High?
│   │   │   ├── Yes → CRITICAL priority
│   │   │   │   ├── Is the device at a trust boundary?
│   │   │   │   │   ├── Yes → Immediate remediation (< 72 hours)
│   │   │   │   │   └── No → Remediate within 2 weeks
│   │   │   │   └── Is there a compensating control?
│   │   │   │       ├── Yes → Document, schedule remediation
│   │   │   │       └── No → Escalate to ISSO
│   │   │   └── No (enhancement) → LOW priority, document in POA&M
│   │   │
│   ├── Moderate
│   │   ├── Baseline control?
│   │   │   ├── Yes → HIGH priority
│   │   │   │   └── Remediate within 30 days
│   │   │   └── No → LOW priority, next assessment cycle
│   │   │
│   └── Low
│       ├── Baseline control?
│       │   ├── Yes → MEDIUM priority
│       │   │   └── Remediate within 90 days
│       │   └── No → LOW priority, discretionary
│
├── Multiple gaps in same family?
│   └── Yes → Evaluate systemic issue (e.g., no AAA = multiple AC failures)
│       └── Address root cause, not individual controls
│
└── Gap affects inherited controls?
    ├── Yes → Coordinate with system owner and inherited control provider
    └── No → Device-level remediation within operations team
```

## Report Template

```
NIST COMPLIANCE ASSESSMENT SUMMARY
=====================================
System Name: [system name]
Authorization Boundary: [description]
Impact Level: [Low / Moderate / High] (FIPS 199)
Framework: [NIST SP 800-53 Rev 5 / CSF 2.0 / Both]
Assessment Date: [timestamp]
Performed By: [assessor/agent]

SYSTEM CATEGORIZATION:
  Confidentiality: [Low / Moderate / High]
  Integrity:       [Low / Moderate / High]
  Availability:    [Low / Moderate / High]
  Overall:         [Low / Moderate / High] (high-water mark)

DEVICES ASSESSED:
  [hostname] — [platform] [version] — [role]

CONTROL FAMILY COMPLIANCE SUMMARY:
  Access Control (AC):                     [n] pass / [n] fail / [n] N/A ([%])
  Audit and Accountability (AU):           [n] pass / [n] fail / [n] N/A ([%])
  Configuration Management (CM):           [n] pass / [n] fail / [n] N/A ([%])
  Identification and Authentication (IA):  [n] pass / [n] fail / [n] N/A ([%])
  System and Comms Protection (SC):        [n] pass / [n] fail / [n] N/A ([%])
  System and Info Integrity (SI):          [n] pass / [n] fail / [n] N/A ([%])
  Overall:                                 [n] pass / [n] fail / [n] N/A ([%])

CSF FUNCTION MAPPING:
  Protect (PR): [controls mapped] — [compliance %]
  Detect (DE):  [controls mapped] — [compliance %]

GAP ANALYSIS:
1. [Severity] [Control ID] — [Control Name]
   Family: [AC/AU/CM/IA/SC/SI]
   CSF Function: [PR/DE]
   Finding: [what was observed]
   Baseline: [L/M/H applicability]
   Compensating Control: [if any]

POA&M (Plan of Action & Milestones):
  Item: [Control ID gap]
  Milestone: [remediation action]
  Responsible: [team/individual]
  Target Date: [date]
  Status: [Open / In Progress / Closed]

NEXT ASSESSMENT: [based on posture — Unsatisfactory: 30d, Deficient: 90d,
                  Conditional: 180d, Satisfactory: 365d]
```

## Troubleshooting

### Mapping CSF Subcategories to 800-53 Controls

CSF subcategories (e.g., PR.AC-1, DE.CM-1) map to multiple 800-53 controls.
Use the NIST SP 800-53 Rev 5 crosswalk (in the control catalog appendices)
to translate between frameworks. When assessing CSF compliance, aggregate
800-53 control results per CSF subcategory — a single control failure does
not necessarily mean the subcategory is fully non-compliant.

### Inherited Controls vs Device-Specific Controls

In shared infrastructure, some controls are inherited from the hosting
environment (e.g., PE controls from a data center, PS controls from the
organization). Distinguish between controls the device implements directly
and controls inherited from external providers. Document inherited controls
with the responsible entity and verification method.

### Multi-Device Scope Aggregation

When multiple devices share an authorization boundary, aggregate findings at
the system level. A control is only fully satisfied when all in-scope devices
implement it — one device failing AC-2 means the system has an AC-2 gap.
Roll up device-level results into the system POA&M.

### Rev 4 vs Rev 5 Differences

NIST 800-53 Rev 5 (2020) restructured controls from Rev 4: controls are no
longer scoped to federal systems only, the Privacy (PT) family was added,
and many controls were consolidated. When working with Rev 4 baselines, use
the NIST-published crosswalk to map Rev 4 IDs to Rev 5 equivalents. Key
network-relevant changes: AC-2 and AU-2 gained enhancements, SC-7 expanded.

### System Categorization Uncertainty

If the system's FIPS 199 categorization is unknown or disputed, the assessor
cannot determine the correct control baseline. Escalate to the system owner
or Information System Security Officer (ISSO) to confirm categorization
before proceeding. Assessing against the wrong impact level produces either
false confidence (Low baseline applied to a High system) or unnecessary
effort (High baseline applied to a Low system).
