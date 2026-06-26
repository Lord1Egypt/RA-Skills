# PAN-OS Security Policy Evaluation Chain

Reference for the PAN-OS packet processing pipeline, zone architecture, policy
matching logic, and Security Profile Group inspection order. This documents
how PAN-OS evaluates traffic from ingress to egress — the foundation for
understanding why policy audit findings matter.

## Packet Processing Pipeline

```
Ingress Interface
       │
       ▼
┌─────────────────┐
│  Zone Lookup     │  Determine ingress zone from interface assignment
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Zone Protection │  Flood protection, recon detection, packet-based
│  Profile Check   │  attack checks (applied BEFORE policy lookup)
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Session Lookup  │  Existing session? → Fast-path to egress
└────────┬────────┘
         │ (new session)
         ▼
┌─────────────────┐
│  NAT Policy      │  Destination NAT evaluated before security policy
│  (Pre-NAT)       │  Security rules match on pre-NAT addresses
└────────┬────────┘
         │
         ▼
┌─────────────────────────────────────────────┐
│  Security Policy Lookup                      │
│                                              │
│  Match criteria (evaluated in rule order):   │
│  - Source Zone + Destination Zone            │
│  - Source Address + Destination Address      │
│  - Application (App-ID)                      │
│  - Service (port/protocol)                   │
│  - User/Group (User-ID)                      │
│  - URL Category (for URL-based policies)     │
│  - HIP Profile (GlobalProtect host state)    │
│                                              │
│  First matching rule wins (top-down)         │
└────────┬────────────────────────────────────┘
         │
         ▼
┌─────────────────┐
│  Action          │
│  Allow / Deny /  │
│  Drop / Reset    │
└────────┬────────┘
         │ (if Allow)
         ▼
┌─────────────────────────────────────────────┐
│  App-ID Identification Chain                 │
│                                              │
│  Phase 1: L4 Session Setup                   │
│  - Initial classification by port/protocol   │
│  - Policy match may use "any" application    │
│                                              │
│  Phase 2: App-ID (L7 Identification)         │
│  - Application signatures applied            │
│  - App shifts: initial app → actual app      │
│  - Policy re-evaluated on app shift          │
│  - Example: TCP/443 → ssl → web-browsing    │
│                                              │
│  Phase 3: Content-ID                         │
│  - Payload inspection after App-ID           │
│  - Threat signatures, data patterns          │
│                                              │
│  Phase 4: URL-ID                             │
│  - URL categorization for web traffic        │
│  - PAN-DB cloud lookup for unknown URLs      │
└────────┬────────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────────────┐
│  Security Profile Processing                 │
│  (Applied in this order on allowed traffic)  │
│                                              │
│  1. Antivirus (AV)                           │
│     → File-based malware detection           │
│     → Stream-based scanning                  │
│                                              │
│  2. Anti-Spyware (AS)                        │
│     → C2 communication detection             │
│     → DNS sinkholing for known-bad domains   │
│     → Spyware phone-home signature matching  │
│                                              │
│  3. Vulnerability Protection (VP)            │
│     → Exploit detection (IPS)                │
│     → Brute-force protection                 │
│     → Protocol anomaly detection             │
│                                              │
│  4. URL Filtering (URL)                      │
│     → Category-based allow/block/alert       │
│     → Credential phishing detection          │
│     → HTTP header logging                    │
│                                              │
│  5. File Blocking (FB)                       │
│     → File type enforcement by direction     │
│     → Block/alert on specific file types     │
│                                              │
│  6. WildFire Analysis (WF)                   │
│     → Unknown file submission to sandbox     │
│     → Verdict: benign/grayware/malware       │
│     → Signature generation for new malware   │
│                                              │
│  7. Data Filtering (DP) — optional           │
│     → DLP pattern matching (SSN, CC, custom) │
│     → Keyword/regex detection                │
└────────┬────────────────────────────────────┘
         │
         ▼
┌─────────────────┐
│  Source NAT      │  Post-policy NAT applied
│  (Post-NAT)     │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Egress Zone     │  Forward to egress interface
│  Forwarding      │
└─────────────────┘
```

## Zone Types

| Zone Type | Function | Common Use |
|-----------|----------|------------|
| **L3** | Routed zone with IP addresses on interfaces | Standard firewall segmentation — LAN, WAN, DMZ |
| **L2** | Switched zone — interfaces in bridge domain | Transparent firewall insertion, same-subnet inspection |
| **V-Wire** | Virtual wire — bump-in-the-wire, no IP config | Inline deployment without IP readdressing |
| **Tap** | Passive monitoring — receives mirrored traffic | Visibility-only deployment, no inline blocking |
| **Tunnel** | Logical zone for tunnel interfaces (IPSec, GRE, GP) | VPN traffic segmentation, GlobalProtect user zones |
| **External** | Virtual system boundary zone (multi-vsys only) | Inter-vsys routing and policy |

## Policy Rule Matching

### Evaluation Order

PAN-OS evaluates security policy rules **top-down, first-match**. The first
rule whose criteria match all fields of the traffic flow is applied. No
further rules are evaluated.

### Rule Types

| Rule Type | Zone Matching | Default Behavior |
|-----------|--------------|------------------|
| **Universal** | Matches both intrazone and interzone traffic | Applies to any zone pair combination |
| **Interzone** | Source zone ≠ destination zone only | Does not match traffic within the same zone |
| **Intrazone** | Source zone = destination zone only | Does not match cross-zone traffic |

### Default Rules (Implicit)

Two implicit rules exist at the bottom of every rulebase:

1. **Intrazone-default:** Action = **allow** — traffic within the same zone
   is permitted by default (no logging, no Security Profiles)
2. **Interzone-default:** Action = **deny** — traffic between different zones
   is denied by default

These defaults are editable — best practice is to enable logging on both
and add Security Profile Groups to the intrazone-default allow.

### App-ID and Policy Re-evaluation

When App-ID identifies the actual application (app shift), PAN-OS
re-evaluates the security policy with the now-known application. This means:

- A session initially matching Rule A (with `application any`) may shift to
  match Rule B (with a specific App-ID) after identification completes
- If no rule matches the shifted application, the session is dropped
- Rules should account for dependent applications (e.g., `web-browsing`
  depends on `ssl` — both must be permitted or use App-ID dependencies)

## Security Profile Group Components

A Security Profile Group bundles individual profiles into a single
assignable object. Binding a group to a rule applies all component profiles.

| Component | What It Inspects | Key Settings |
|-----------|-----------------|--------------|
| **Antivirus** | File transfers across protocols (HTTP, SMTP, FTP, SMB, IMAP, POP3) | Decoder actions per protocol, WildFire inline ML |
| **Anti-Spyware** | DNS queries, HTTP headers, connection patterns for C2/spyware signatures | DNS Security, sinkhole action, passive DNS monitoring |
| **Vulnerability Protection** | Protocol-level exploit attempts, brute-force patterns | Severity-based action (alert/drop/reset), CVE coverage |
| **URL Filtering** | HTTP/HTTPS URL categories, credential submission sites | Category actions (allow/alert/block/continue/override) |
| **File Blocking** | File types by application and direction (upload/download/both) | Block vs alert, specific file type granularity |
| **WildFire Analysis** | Unknown/unclassified files submitted for sandbox analysis | File size limits, submission protocols, verdict actions |
| **Data Filtering** | Content patterns: credit cards, SSNs, custom data patterns | Pattern matching thresholds, per-application granularity |

## Panorama Device Group Hierarchy

In Panorama-managed deployments, security policy evaluation follows the
device group hierarchy:

```
Shared Pre-Rules           ← Highest priority, enterprise-wide policy
       │
       ▼
Device-Group Pre-Rules     ← Site/function-specific mandatory policy
       │
       ▼
Local Firewall Rules       ← Rules configured directly on the firewall
       │
       ▼
Device-Group Post-Rules    ← Site/function-specific default policy
       │
       ▼
Shared Post-Rules          ← Lowest priority, enterprise-wide defaults
       │
       ▼
Implicit Rules             ← intrazone-default (allow), interzone-default (deny)
```

### Hierarchy Implications for Audit

- **Pre-rules** cannot be overridden by local firewall admins — use for
  mandatory security policy (e.g., block known-bad categories, require
  Security Profiles on internet-bound traffic)
- **Post-rules** provide defaults that local admins can override with
  local rules — use for baseline policy that sites may need to customize
- **Shared** scope applies to all device groups; **device-group** scope
  applies only to firewalls in that group
- An audit must evaluate the **effective merged rulebase** on each target
  firewall, not just the Panorama configuration in isolation

## Decryption Policy

Decryption policy is evaluated separately from security policy but directly
affects Security Profile efficacy:

| Decryption Type | Direction | Function |
|-----------------|-----------|----------|
| **SSL Forward Proxy** | Outbound | Decrypts client-initiated TLS to external servers; re-encrypts with proxy CA |
| **SSL Inbound Inspection** | Inbound | Decrypts TLS to internal servers using the server's certificate/key |
| **SSH Proxy** | Both | Decrypts SSH sessions for content inspection |
| **No Decrypt** | Both | Explicitly excludes traffic from decryption (compliance, technical limitations) |

Without decryption, Security Profiles can only inspect:
- Connection metadata (IP, port, SNI, certificate fields)
- DNS queries (Anti-Spyware DNS Security)
- Application identification via TLS handshake (App-ID still functions)

Encrypted payload content (file transfers, URL paths, exploit payloads) remains
opaque to Security Profiles without decryption enabled.
