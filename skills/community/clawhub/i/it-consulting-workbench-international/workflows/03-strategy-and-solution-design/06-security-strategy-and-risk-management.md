# Cybersecurity Strategy & Risk Management

## Objectives

Design an enterprise security strategy, conduct security maturity assessment based on the NIST CSF 2.0 framework, identify key risks and control measures, and develop a security investment roadmap.

---

## Prerequisites
- IT current state diagnostic report completed (including security dimension)
- Understanding of the client industry's compliance requirements (Information Security Protection Levels / ISO 27001 / SOC2 / industry regulations)
- Understanding of the client's business risk appetite

## Inputs
- IT current state diagnostic report (security architecture / security operations / security incident history)
- Industry regulatory compliance checklist
- Existing security investments and tools inventory
- IT strategy / cloud strategy direction (security must be designed in collaboration with architecture)

---

## Operation Steps

### Step 1: Security Risk Context Establishment

**Output**: Security Context Document

#### 1.1 Identify the "Crown Jewels"

List the client's 5-7 most important digital assets:

| Asset | Type | Why Important | Impact of Breach | Attacker Profile |
|------|------|----------|------------|----------|
| Customer PII Data | Data | 20M user privacy | Regulatory fines + reputation collapse + class action | Black market / Insiders |
| Core Transaction System | System | 100K transactions/sec | Business interruption, $X loss per minute | Ransomware / APT |
| Core Algorithm Model | IP | 3 years R&D, $X invested | Loss of competitive advantage | Corporate espionage |
| ... |

#### 1.2 Risk Appetite Statement

```
We are willing to accept:
- [ ] Low-impact single-point failures (e.g., non-core system downtime <2 hours)
- [ ] Low-frequency low-impact security incidents (e.g., phishing emails <5/month avg)

We are NOT willing to accept:
- [x] Customer data breach (regardless of scale)
- [x] Core transaction system downtime exceeding 15 minutes
- [x] Regulatory penalties / license impact
- [x] Reputation damage leading to >5% customer churn
```

---

### Step 2: Security Maturity Assessment (NIST CSF 2.0)

**Output**: Security maturity scorecard + gap analysis

#### 2.1 NIST CSF 2.0 Six-Function Scoring

For each subcategory under each function, score 1 (Initial) to 5 (Optimized):

```
Govern — New in NIST 2.0
├── Organization Context                 [1-5]
├── Risk Management Strategy             [1-5]
├── Supply Chain Risk                    [1-5]
├── Roles & Responsibilities             [1-5]
├── Policies & Processes                 [1-5]
└── Oversight                            [1-5]

Identify
├── Asset Management                     [1-5]
├── Risk Assessment                      [1-5]
└── Improvement                          [1-5]

Protect
├── Identity & Access                    [1-5]
├── Awareness & Training                 [1-5]
├── Data Security                        [1-5]
├── Platform Security                    [1-5]
└── Infrastructure Resilience            [1-5]

Detect
├── Continuous Monitoring                [1-5]
└── Adverse Event Analysis               [1-5]

Respond
├── Incident Management                  [1-5]
├── Incident Analysis                    [1-5]
└── Incident Response & Recovery Communication  [1-5]

Recover
├── Recovery Plan Execution              [1-5]
└── Restoration Communication            [1-5]
```

#### 2.2 Gap Analysis Prioritization

Gap = Target Level (based on industry and risk appetite) - Current Level:

| Security Domain | Current | Target | Gap | Priority | Est. Investment |
|--------|------|------|------|--------|---------|
| Supply Chain Security | 1 (No assessment) | 3 (Has process) | 2 | High | $0.3M |
| Identity Management | 2 (Has AD) | 4 (MFA+Zero Trust) | 2 | High | $0.5M |
| Continuous Monitoring | 2 (Has logs) | 4 (SIEM+SOAR) | 2 | High | $1M |
| ... |

---

### Step 3: Security Architecture Design

#### 3.1 Layered Security Architecture

```
┌─────────────────────────────────────────────────┐
│  Security Governance Layer: Security Policy / Risk Mgmt / Compliance Audit / Security Awareness │
├─────────────────────────────────────────────────┤
│  Identity Security: SSO + MFA + PIM/PAM + Zero Trust Network     │
├─────────────────────────────────────────────────┤
│  Data Security: Classification / Encryption / Masking / DLP / Audit    │
├─────────────────────────────────────────────────┤
│  Application Security: SAST/DAST/SCA/WAF/API Security           │
├─────────────────────────────────────────────────┤
│  Infrastructure Security: Firewall/IDS/IPS/Endpoint Security/Container Security │
├─────────────────────────────────────────────────┤
│  Detection & Response: SIEM + SOAR + EDR + XDR + MDR     │
├─────────────────────────────────────────────────┤
│  Physical & Environmental Security: Data Center/Office/ICS Physical Security │
└─────────────────────────────────────────────────┘
```

#### 3.2 Zero Trust Architecture Deep Dive (Based on NIST SP 800-207)

##### Three Core Principles (NIST SP 800-207)
1. **Never Trust, Always Verify**: Every access request requires re-authentication + re-authorization
2. **Least Privilege**: Grant only the minimum privilege needed to complete the task (Just-in-Time + Just-Enough Access)
3. **Assume Breach**: All traffic encrypted, micro-segmentation, continuous monitoring

##### Three Technical Paths Explained
| Path | Technical Principle | Representative Vendors | Implementation Priority |
|------|---------|---------|----------|
| **SASE** | Cloud-native security + SD-WAN convergence | Zscaler, Netskope, Sangfor | Year 1 Q4 |
| **ZTNA** | Application-level encrypted tunnel replacing VPN | Zscaler ZPA, Cloudflare Access | Year 1 Q2 |
| **Micro-segmentation** | Fine-grained access control between workloads | Illumio, Guardicore, NSX | Year 2 Q2 |

##### 2026 Zero Trust Trends
- **AI-driven Adaptive Policies**: Dynamically adjust access permissions based on real-time risk scoring
- **Identity Threat Detection & Response (ITDR)**: Identity systems themselves become an attack surface; ITDR becomes an independent category
- **OT/IoT Zero Trust Framework Maturity**: Manufacturing/energy OT environment Zero Trust deployment guidelines maturing

##### Zero Trust Implementation Roadmap
```
Year 1: Foundation — Mandatory MFA + Identity Governance + Device Compliance + ZTNA Pilot
Year 2: Expansion — Micro-segmentation + Data Classification + AI Adaptive Policies
Year 3: Maturity — Full enterprise coverage + AI-driven Continuous Adaptive Authentication
```

##### Zero Trust Key KPIs
| KPI | M6 Target | M12 Target | M24 Target |
|-----|--------|---------|---------|
| MFA Coverage | 80% | 100% | 100% |
| Lateral Movement Detection | <24h | <1h | <5min |
| Anomalous Access Auto-Block | 30% | 60% | 90% |

##### Zero Trust Three Pillars

1. Identity = New Perimeter
   - Never trust, always verify
   - Authenticate + authorize every access
   - Least privilege (Just-in-Time, Just-Enough)
   - Multi-factor authentication (MFA) mandatory

2. Device = Access Prerequisite
   - Device compliance check
   - Device health score
   - Unhealthy devices auto-isolated

3. Network = Default Untrusted
   - Micro-segmentation
   - Applications cannot communicate by default, explicit allow only
   - Traffic encryption (even on internal network)

#### 3.3 OT/IT Security Convergence (For Manufacturing/Energy)

```
OT-Specific Security Challenges:
├── Availability > Confidentiality (IT: Confidentiality > Availability)
├── Systems cannot be taken offline for patching (planned maintenance windows needed)
├── Non-standard protocols (Modbus/OPC/Profinet, no encryption)
└── Equipment lifespan 15-20 years (IT equipment 3-5 years)

OT/IT Security Convergence Strategy:
├── Industrial DMZ: Security buffer zone between IT and OT
├── Unidirectional Gateway: Data flows only from OT to IT, no reverse allowed
├── OT Network Visibility: Passive traffic analysis (no active scanning, which may cause equipment failure)
└── OT-Specific Endpoint Protection: Lightweight / no impact on real-time control
```

---

### Step 4: Security Operations Design

#### 4.1 Security Operations Maturity

| Level | Characteristics | Target |
|------|------|------|
| L1: Reactive | Incident → Respond, no proactive monitoring | — |
| L2: Proactive | Has monitoring, has processes, has on-call | MTTD <24 hours |
| L3: Predictive | Threat intelligence + hunting, automated response | MTTD <1 hour, MTTR <4 hours |
| L4: Adaptive | AI-driven + automated, continuous assessment | MTTD <1 minute, MTTR <30 minutes |

#### 4.2 SOC Build Model Selection

| Model | Description | Applicable | Annual Cost (Reference) |
|------|------|------|------------|
| Self-built SOC | Fully self-built, 7×24 | Large enterprises (>10,000 people) | $2-5M |
| Hybrid SOC | Self-built security team + MDR managed | Mid-size enterprises | $0.5-2M |
| Managed MDR | Fully outsourced SOC | SMBs | $0.1-0.5M |

#### 4.3 Core Security Operations Processes

Minimum essential security processes that must be formally established:

1. **Incident Response Process (IRP)**: Detect → Triage → Contain → Eradicate → Recover → Post-mortem
2. **Vulnerability Management Process**: Discover → Assess → Prioritize → Remediate → Verify
3. **Change Management (Security-related)**: Security Review → Test → Gradual Rollout → Rollback
4. **Access Review Process**: Regular permission review → Anomalous permission investigation → Permission revocation
5. **Security Awareness Training**: Onboarding training → Monthly phishing tests → Annual assessment

---

### Step 5: Vendor/Supply Chain Security Management

#### 5.1 Vendor Security Tiering

| Risk Level | Definition | Security Requirements | Example |
|---------|------|---------|------|
| **High** | Can access core systems/data | On-site audit + penetration test + SOC2 Type II | Core system outsourced O&M |
| **Medium** | Can access non-core data | Security questionnaire + compliance certification + annual reassessment | Recruitment system SaaS |
| **Low** | No data access | Security questionnaire (simplified) | Cafeteria management SaaS |

#### 5.2 Vendor Security Review Checklist

```
□ Has security certification? (SOC2/ISO27001/Information Security Protection Levels)
□ Where is data stored? Does it cross borders?
□ Who can access our data? Any subcontractors?
□ How often are penetration tests done? Can we see a report summary?
□ Any security incidents in the past 12 months? How were they handled?
□ If a security incident occurs, how quickly are we notified?
□ Upon contract expiry/termination, how is data destroyed?
□ Is there BCP/DR? What SLAs are in place?
```

---

### Step 6: Security Investment & Roadmap

#### 6.1 Security Investment Benchmarks

- Security spend as % of total IT spend: 5-10% (Financial/government higher, 10-15%)
- People:Tools:Services ≈ 40:30:30 (world-class security organization)
- Security staff as % of total IT staff: 5-10%

#### 6.2 Three-Year Security Roadmap

```
Year 1: Fix the Basics
├── Identity Security: MFA mandatory (all staff), SSO, PAM
├── Asset Visibility: Inventory all internet-exposed assets
├── Patch Management Process: Critical vulnerabilities <7 days remediation
├── EDR Deployment: All endpoints
├── Security Awareness: All-staff training + phishing tests
├── Incident Response: Establish formal IRP + drill (1 tabletop exercise)
└── Investment: $[X]M

Year 2: Build Defenses
├── SIEM+SOAR Go live
├── Zero Trust Step 1 (core systems)
├── Data Security: Classification + DLP
├── Supply Chain Security formalized
├── Red Team exercises (once every 6 months)
├── SOC maturity to L2
└── Investment: $[X]M

Year 3: Optimize & Automate
├── AI-driven threat detection
├── Zero Trust expanded to entire enterprise
├── Automated incident response (70% Level 1 incidents auto-handled)
├── Continuous supply chain monitoring
├── SOC maturity to L3
└── Investment: $[X]M
```

---

## Outputs
1. **Security Context Document**: Crown jewels + risk appetite
2. **NIST CSF 2.0 Maturity Assessment**: Scores + gap analysis
3. **Security Architecture Design**: Layered architecture + Zero Trust + OT security (if applicable)
4. **Security Operations Design**: SOC model + core processes
5. **Supply Chain Security Framework**: Tiering criteria + review checklist
6. **Security Investment Roadmap**: Three-year plan + investment + milestones

---

## Quality Check
- [ ] "Crown jewel" assets clearly identified and confirmed by stakeholders
- [ ] Security maturity assessment uses standard framework (NIST CSF 2.0), not a custom framework
- [ ] Each security control recommendation directly maps to an identified risk
- [ ] OT security considered (if client is manufacturing/energy)
- [ ] Security operations design is not just "buy a SIEM and done" — includes process and people design
- [ ] Vendor security has tiering, not "all vendors fill out the same questionnaire"
- [ ] Roadmap has Quick Wins (visible results needed by Year 1 Q1)

---

## Common Pitfalls

| Pitfall | Why It's Wrong | Correct Approach |
|------|---------|---------|
| "Buy more security tools" | Tool stacking ≠ security; without processes and people operating them = expensive decorations | Define processes and people first, then buy tools; every tool purchased must have someone using it |
| Security = IT Security | Security is a business issue, not a technology issue | Board-level security reporting, speak about security risk in business language |
| Ignoring insider threats | Most security budget goes to defending against external attacks, but insider (intentional/unintentional) leaks account for >30% | Least privilege + behavioral anomaly detection + offboarding security checks |
| Security blocking business | "This is not secure, can't do it" → business bypasses IT and does it themselves | Security team role transformation: from "No" to "How to do it safely" |
| Paper compliance | Certification passed ≠ secure; many enterprises have ISO27001 but poor actual security | Compliance = minimum standard; real security requires continuous improvement |
| Ignoring low-probability high-impact events | "We're not an APT target" → but your suppliers might be | At minimum: security assessment of the 3-5 most critical suppliers |