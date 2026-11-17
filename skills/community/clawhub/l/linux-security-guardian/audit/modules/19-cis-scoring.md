# Module 19 — CIS Benchmark Scoring Summary

## Purpose
Calculate CIS (Center for Internet Security) benchmark alignment percentage across all audit modules. Provides a single compliance score per server and identifies the biggest gaps.

## Scoring Methodology

### Weighted Scoring
Each module contributes to the CIS score based on its CIS benchmark weight:

| Module | CIS Category | Weight | Max Score |
|--------|-------------|--------|-----------|
| 01-system | 1 — Initial Setup | 5% | 5 |
| 02-users | 5 — Access Control | 10% | 10 |
| 03-ssh | 5 — Access Control | 10% | 10 |
| 04-auth | 5 — Access Control | 10% | 10 |
| 05-services | 2 — Services | 5% | 5 |
| 06-packages | 3 — Software Updates | 10% | 10 |
| 07-cve | 3 — Software Updates | 5% | 5 |
| 08-network | 4 — Network | 5% | 5 |
| 09-firewall | 4 — Network | 10% | 10 |
| 10-filesystem | 1 — Initial Setup | 5% | 5 |
| 11-kernel | 1 — Initial Setup | 5% | 5 |
| 12-logs | 6 — Logging | 5% | 5 |
| 13-crons | 1 — Initial Setup | 2% | 2 |
| 14-ssl | 4 — Network | 3% | 3 |
| 15-docker | 7 — Containers | 5% | 5 |
| 16-disk | 1 — Initial Setup | 2% | 2 |
| 17-integrity | 6 — Logging | 2% | 2 |
| 18-rootkit | 6 — Logging | 1% | 1 |
| 20-systemd-analyze | 2 — Services | 2% | 2 |
| 21-mount-hardening | 1 — Initial Setup | 3% | 3 |
| 22-apparmor-selinux | 1 — Initial Setup | 5% | 5 |
| 23-proc-hidepid | 1 — Initial Setup | 3% | 3 |
| 24-swap-encryption | 1 — Initial Setup | 3% | 3 |
| 25-usbguard | 1 — Initial Setup | 2% | 2 |
| 26-ipv6-audit | 4 — Network | 3% | 3 |
| **Total** | | **121% → scaled to 100%** | **121** |

### Scoring Rules
- **PASS** → Full weight
- **WARN/MEDIUM** → 50% weight
- **HIGH/CRITICAL** → 0% weight
- **SKIP** (module not applicable) → Excluded from calculation (weight redistributed)

### CIS Level Classification
| Score | CIS Level | Meaning |
|-------|-----------|---------|
| 90-100% | L1 — Foundational | Basic security hygiene met |
| 70-89% | L2 — Intermediate | Good security posture |
| 50-69% | L3 — Advanced | Significant gaps remain |
| 25-49% | L4 — High Risk | Multiple critical gaps |
| 0-24% | L5 — Critical | Urgent action needed |

## Commands
```bash
# No direct commands — score is calculated from all module results
# This module aggregates findings from modules 01-18

# Check CIS benchmark documentation availability
ls /usr/share/doc/cis-benchmark* 2>/dev/null || echo "cis_docs_not_found"
```

## Scoring Calculation

### Per-Module Scoring
```
module_score = module_weight × pass_ratio

Where:
- pass_ratio = pass_count / (pass_count + warn_count + fail_count)
- warn_count = findings with MEDIUM severity
- fail_count = findings with HIGH or CRITICAL severity
- pass_count = findings with PASS or LOW severity
```

### Total Score
```
total_score = sum(module_score for all modules) / sum(module_weight for scored modules) × 100
```

### Gap Analysis
Top 3 modules with lowest scores → priority improvement targets.

## Output Format
```
[INFO] 19-cis: score | total: 72% | level: L2 — Intermediate
[INFO] 19-cis: top_gaps | 1: 03-ssh (40%) | 2: 04-auth (50%) | 3: 15-docker (60%)
[INFO] 19-cis: module_scores | 01-system: 100% | 02-users: 80% | 03-ssh: 40% | 04-auth: 50% | ...
[INFO] 19-cis: pass_count: 45 | warn_count: 12 | fail_count: 8 | total_checks: 65
```

## CIS Level Summary

### L1 — Foundational (90-100%)
- ✅ Basic security hygiene
- ✅ No critical gaps
- ✅ Regular patching
- ✅ SSH hardened
- ✅ Firewall active

### L2 — Intermediate (70-89%)
- ⚠️ Some gaps in access control
- ⚠️ Password policy may need tightening
- ⚠️ Logging may be incomplete
- ✅ Core security in place

### L3 — Advanced (50-69%)
- ⚠️ Multiple significant gaps
- ⚠️ SSH or auth needs hardening
- ⚠️ File integrity not configured
- ⚠️ Audit logging incomplete

### L4 — High Risk (25-49%)
- 🔴 Critical gaps in multiple areas
- 🔴 SSH or firewall misconfigured
- 🔴 No file integrity monitoring
- 🔴 Password policy weak or absent

### L5 — Critical (0-24%)
- 🚨 Urgent action required
- 🚨 Multiple critical vulnerabilities
- 🚨 No security controls in place
- 🚨 Immediate remediation needed

## Auto-Report
After scoring, include in audit report:
```markdown
## CIS Benchmark Summary
- **Score:** 72% (L2 — Intermediate)
- **Top 3 Gaps:** 03-ssh (40%), 04-auth (50%), 15-docker (60%)
- **Recommendation:** Focus on SSH hardening and authentication controls
- **Next Target:** L1 — Foundational (90%+)
```
