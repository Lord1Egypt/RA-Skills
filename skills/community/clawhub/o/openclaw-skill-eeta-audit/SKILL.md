---
name: eeat-openclaw-skill-audit
description: OpenClaw Skill quality audit based on CORE-EEAT framework adapted for AI agent skills. Evaluates skill's utility (task completion efficiency) and security (safe execution). Features 80 standardized criteria, 8-dimension scoring, veto item detection for security vulnerabilities, and priority improvement recommendations. Applicable for skill selection, security vetting, and skill quality assessment.
---

# EEAT OpenClaw Skill Audit

> **AI Agent Skill Quality Assurance** — This skill adapts the CORE-EEAT framework to evaluate OpenClaw Skills, ensuring they deliver meaningful utility while maintaining security and reliability.

## Skill Overview

OpenClaw Skills are modular capability extensions for AI agents, defined by `SKILL.md` files with YAML frontmatter and prompt instructions. This skill evaluates skill quality through 80 standardized criteria across 8 core dimensions, generating comprehensive audit reports including utility scores, security assessments, and actionable improvement recommendations.

**Core Transformation**:
- **From**: Install Skills blindly → Hope they work
- **To**: Systematic vetting → Data-driven skill selection

## OpenClaw Skill Structure

Every OpenClaw Skill consists of:

```
my-skill/
├── SKILL.md          # Core definition (YAML + Markdown instructions)
├── scripts/          # Optional executable scripts
│   └── main.py
└── references/       # Optional configuration and resources
    └── config.json
```

**Key Components**:
- **YAML Frontmatter**: Skill metadata (name, description, version, dependencies, gates)
- **Prompt Instructions**: How the AI should use this skill
- **Scripts**: Optional executable code for complex operations
- **Gating Mechanism**: Conditional activation (bins, env, os checks)

## Applicable Scenarios

Use this skill when users request:

### Skill Selection
- "Evaluate this skill before installing"
- "Compare two skills for the same task"
- "Which skill should I use for X?"

### Security Vetting
- "Is this skill safe to run?"
- "Scan for security vulnerabilities"
- "Check permission boundaries"

### Skill Development
- "Audit my skill for quality issues"
- "How to improve my skill's documentation?"
- "What security best practices am I missing?"

### Skill Maintenance
- "Review installed skills for quality"
- "Identify deprecated or risky skills"
- "Prioritize skill updates"

## Core Capabilities

This skill can:

1. **Complete 80-Item Audit**: Score each CORE-EEAT item adapted for OpenClaw Skills

2. **Utility Scoring**: Evaluate task completion efficiency and comparative value

3. **Security Assessment**: Three-level security evaluation (Pass/Caution/Risk)

4. **Gating Validation**: Check conditional activation requirements (bins, env, os)

5. **Veto Item Detection**: Flag critical security violations (command injection, data leakage)

6. **Priority Ranking**: Identify top 5 improvements by impact

7. **Comparative Analysis**: Compare skills for same use case

## Skill Categories

This skill supports 6 OpenClaw Skill types, each with different evaluation priorities:

### Productivity Skills
- **Definition**: Gmail, Calendar, Google Drive, Microsoft Office integration
- **Focus**: Task completion accuracy, API reliability, error handling
- **Weights**: C: 30% | R: 25% | Exp: 20% | Ept: 15% | O: 5% | E: 0% | A: 5% | T: 0%

### Development Skills
- **Definition**: Code generation, debugging, GitHub automation, CI/CD
- **Focus**: Code quality, correctness, testing, security best practices
- **Weights**: C: 25% | O: 20% | R: 20% | Ept: 20% | E: 5% | Exp: 5% | A: 5% | T: 0%

### Research Skills
- **Definition**: Web search, web fetch, document summarization, data analysis
- **Focus**: Information accuracy, source credibility, citation quality
- **Weights**: C: 25% | R: 25% | A: 20% | E: 15% | O: 10% | Exp: 0% | Ept: 0% | T: 5%

### Automation Skills
- **Definition**: Browser automation, file operations, shell commands, task scheduling
- **Focus**: Security, error handling, robustness, permissions
- **Weights**: T: 30% | C: 25% | R: 20% | O: 15% | Exp: 5% | Ept: 5% | E: 0% | A: 0%

### Content Skills
- **Definition**: Text generation, translation, image generation, audio processing
- **Focus**: Output quality, style consistency, creative value
- **Weights**: C: 30% | E: 25% | Exp: 20% | O: 15% | Ept: 5% | R: 5% | A: 0% | T: 0%

### System Skills
- **Definition**: System monitoring, resource management, network tools, debugging
- **Focus**: Performance, reliability, security, compatibility
- **Weights**: T: 25% | C: 20% | R: 20% | E: 15% | O: 10% | Ept: 5% | Exp: 5% | A: 0%

---

## 8 Progressive Quality Gates

### Gate 1: Metadata Validation (Pre-Installation)

**When**: Before installing any skill

**Duration**: 2-5 minutes

**Items**:
- **C01**: YAML frontmatter present and valid
- **C02**: Skill name and description clear
- **O01**: Skill structure follows OpenClaw convention
- **T04**: No suspicious dependencies or permissions

**Deliverable**: Metadata Validation Report

**Failure**: Do not install. Contact skill author or fix manually.

---

### Gate 2: Gating Mechanism Check

**When**: After metadata validation, before activation

**Duration**: 1-2 minutes

**Items**:
- **O02**: Required tools exist (bins check)
- **O03**: Required environment variables set (env check)
- **O04**: OS compatibility verified (os check)
- **T07**: No conflicting permissions

**Deliverable**: Gating Compatibility Report

**Failure**: Skill will not activate. Fix environment or choose alternative.

---

### Gate 3: Security Pre-Check

**When**: Before first execution

**Duration**: 3-5 minutes

**Items**:
- **T01**: No command injection vulnerabilities
- **T02**: No data leakage risks
- **T03**: Input validation present
- **T04**: Permissions are minimal principle

**Deliverable**: Security Pre-Check Report

**Failure**: Do not execute. Review code or choose alternative.

---

### Gate 4: Prompt Quality Review

**When**: During skill development or installation

**Duration**: 5-10 minutes

**Items**:
- **C03**: Instructions are clear and actionable
- **C04**: Tool usage patterns are explicit
- **Ept03**: Professional terminology used
- **Ept05**: Follows prompt engineering best practices

**Deliverable**: Prompt Quality Report

**Failure**: Skill may misbehave. Refine SKILL.md instructions.

---

### Gate 5: Script Security Audit

**When**: For skills with executable scripts

**Duration**: 10-20 minutes

**Items**:
- **T05**: No hardcoded secrets or API keys
- **T06**: No eval/exec of user input
- **T07**: Proper error handling and logging
- **T08**: Resource cleanup implemented

**Deliverable**: Script Security Audit

**Failure**: Security risk. Audit scripts or avoid skill.

---

### Gate 6: Utility Testing

**When**: During skill evaluation

**Duration**: 15-30 minutes

**Items**:
- **C05**: Completes intended tasks successfully
- **C06**: Output quality meets expectations
- **Exp01**: Usage examples provided and working
- **Exp02**: Performance characteristics documented

**Deliverable**: Utility Test Report

**Failure**: Skill doesn't deliver value. Consider alternatives.

---

### Gate 7: Comparative Analysis

**When**: Selecting between multiple skills for same task

**Duration**: 10-15 minutes

**Items**:
- **E01**: Offers unique value vs alternatives
- **E02**: Better performance or efficiency
- **A01**: Active maintenance and updates
- **A02**: Community adoption and reviews

**Deliverable**: Comparative Analysis Report

**Failure**: Alternative skill may be better. Choose based on scores.

---

### Gate 8: Full 80-Item Audit

**When**: Critical skills, major updates, security reviews

**Duration**: 30-60 minutes

**Items**: All 80 items across all 8 dimensions

**Deliverable**: Comprehensive EEAT Audit Report

**Failure**: Address critical issues before production use.

---

## Usage Examples

### Example 1: Pre-Installation Security Check

**User Request**:
```
Check if this skill is safe to install:
clawhub install agent-browser
```

**Response**:
```markdown
## EEAT Skill Security Audit: agent-browser

### Gate 1: Metadata Validation ✅
- [x] YAML frontmatter valid
- [x] Description clear: "Browser automation for web scraping"
- [x] Version: 1.2.3
- [x] Dependencies: playwright (verified safe)

### Gate 2: Gating Check ⚠️
- [x] Bins: playwright installed
- [x] Env: PLAYWRIGHT_BROWSERS_PATH set
- [ ] OS: macOS/Windows only (Linux limited support)

### Gate 3: Security Pre-Check ✅
- [x] T01: No command injection detected
- [x] T02: No data leakage risks
- [x] T03: Input validation on URLs
- [x] T04: Minimal permissions (browser control only)

### Security Score: 92/100
**Security Status**: CAUTION ⚠️
- Linux support limited
- Requires browser installation (system-level change)

### Recommendation
✅ **Install with Caution**
- Safe for macOS/Windows users
- Linux users should check compatibility
- Review permissions before first use
```

---

### Example 2: Compare Two Skills

**User Request**:
```
Compare tavily-search vs web-search for web search
```

**Response**:
```markdown
## Skill Comparative Analysis: Web Search

### Skill A: tavily-search

**Utility Score**: 85/100
- C05: High accuracy search results ✅
- C06: Clean, structured output ✅
- Exp01: Excellent usage examples ✅
- E01: AI-optimized for agents 🎯

**Security Score**: 95/100
- T01-T04: All checks pass ✅
- T07: No external dependencies ✅

**Overall**: 88/100 (Very Good)

### Skill B: web-search (bundled)

**Utility Score**: 70/100
- C05: Basic search functionality ✅
- C06: Output quality varies ⚠️
- Exp01: Limited examples ⚠️
- E01: Generic implementation ⚠️

**Security Score**: 90/100
- T01-T04: Safe but basic ✅
- T07: Uses external APIs ⚠️

**Overall**: 75/100 (Good)

### Recommendation
✅ **Choose tavily-search**
- +18 points higher utility
- AI-optimized for agent workflows
- Better structured output for downstream processing
- Higher security score

**Trade-off**: Requires API key setup vs. no setup for web-search
```

---

### Example 3: Full Skill Audit

**User Request**:
```
Audit my custom skill: email-automation
[Paste SKILL.md content]
```

**Response**:
```markdown
## EEAT Skill Audit: email-automation

### Overview
- **Skill Type**: Productivity
- **Total Score**: 62/100 (Fair)
- **Utility Score**: 75/100 (Good)
- **Security Score**: 45/100 (CAUTION ⚠️)
- **Veto Item**: ⚠️ T02 Triggered (Data Leakage Risk)

### Dimension Scores

| Dimension | Score | Rating | Weight | Weighted Score |
|-----------|-------|--------|--------|----------------|
| C — Correctness | 70/100 | Good | 30% | 21 |
| O — Organization | 65/100 | Fair | 5% | 3.25 |
| R — Referenceability | 50/100 | Fair | 25% | 12.5 |
| Exp — Experience | 80/100 | Good | 20% | 16 |
| Ept — Expertise | 55/100 | Fair | 15% | 8.25 |
| E — Exclusivity | 40/100 | Poor | 0% | 0 |
| A — Authority | 60/100 | Fair | 5% | 3 |
| T — Trust | 45/100 | Poor | 0% | 0 |
| **Weighted Total** | | | | **64** |

### Critical Issues (Veto Items)

⚠️ **T02: Data Leakage Risk**
**Issue**: Skill stores API credentials in plain text in SKILL.md
```yaml
# SKILL.md
credentials:
  smtp_password: "mypassword123"  # ⚠️ SECURITY RISK
```
**Action**: Move credentials to environment variables
```yaml
credentials:
  smtp_password: "${SMTP_PASSWORD}"  # ✅ SECURE
```

### Top 5 Priority Improvements

1. **T02 Data Leakage** — Remove hardcoded credentials
   - Current: Fail | Potential Gain: 8 weighted points
   - Action: Use environment variables for all secrets

2. **R02 Coverage** — Add error handling examples
   - Current: Fail | Potential Gain: 6.25 weighted points
   - Action: Document error scenarios and recovery

3. **Ept01 Documentation** — Improve prompt instructions
   - Current: Partial | Potential Gain: 4.5 weighted points
   - Action: Add step-by-step usage examples

4. **R03 Source Authority** — Verify email library security
   - Current: Partial | Potential Gain: 3.75 weighted points
   - Action: Audit nodemailer dependency for vulnerabilities

5. **O01 Structure** — Add scripts/ directory for complex logic
   - Current: Partial | Potential Gain: 2.5 weighted points
   - Action: Move complex operations to Python scripts

### Action Plan

#### Quick Wins (Fix immediately)
- [ ] Move all credentials to environment variables
- [ ] Add error handling documentation

#### Medium Investment (This week)
- [ ] Add comprehensive usage examples
- [ ] Implement proper logging in scripts

#### Strategic (Next sprint)
- [ ] Add test suite with edge cases
- [ ] Implement retry logic for failed sends
- [ ] Add HTML email support

### Recommendation
⚠️ **Do Not Install Until Fixed**
- Security risk (T02 veto) must be addressed
- After fixes, expected score: 78/100 (Good)
```

---

## Reference Documents

- `references/openclaw-skill-benchmark.md` — Complete 80-item benchmark adapted for OpenClaw Skills
- `references/skill-security-checklist.md` — Security-specific evaluation criteria
- `references/utility-testing-guide.md` — How to test skill utility and comparative value
- `workflow-optimization-analysis.md` — Adaptation strategy from code to skills

---

## Key Differences: Code vs. Skill Audit

| Aspect | Code Audit | Skill Audit |
|--------|-----------|-------------|
| **Primary Focus** | Code correctness, maintainability | Utility, security, reliability |
| **Security Emphasis** | SQL injection, XSS | Command injection, data leakage, permissions |
| **Evaluation Method** | Static analysis + testing | Comparative utility + security probes |
| **Output Format** | Code quality report | Utility score + security status label |
| **Key Metrics** | Test coverage, complexity | Task completion, risk level |
| **Veto Items** | Security bugs, logic errors | Security vulnerabilities, data risks |
| **Automation Level** | High (linters, type checkers) | Medium (requires manual security review) |
| **Comparative Analysis** | Code vs. requirements | Skill vs. baseline/skills |

---

## Success Points

1. **Security-First Approach** — OpenClaw Skills have system-level access; security is non-negotiable

2. **Comparative Utility** — Evaluate skills relative to baseline, not in isolation

3. **Gating Validation** — Ensure skills only activate when dependencies are met

4. **Prompt Quality** — SKILL.md instructions determine skill behavior; quality matters

5. **Minimal Permissions** — Skills should only request necessary access

6. **Active Maintenance** — Prioritize skills with recent updates and community support

7. **Real-World Testing** — Test with actual use cases, not synthetic scenarios

---

## Optimization Recommendations

Based on OpenClaw's architecture and community best practices:

### 1. Add Skill Registry Integration
- Integrate with ClawHub API for real-time skill metadata
- Auto-fetch version history, update frequency, download counts
- Community signals: stars, issues, last commit date

### 2. Implement Automated Security Scanning
- Integrate with `clawsec` (ClawHub security scanner)
- Auto-scan scripts/ directory for vulnerabilities
- Check for hardcoded secrets, eval/exec patterns

### 3. Add Utility Benchmarking
- Run comparative tests: baseline vs. with-skill
- Measure task completion time, token efficiency, success rate
- Generate utility scores similar to SkillTester framework

### 4. Create Skill Dependency Graph
- Map skill dependencies (some skills require others)
- Detect circular dependencies
- Recommend optimal skill combinations

### 5. Implement Skill Conflict Detection
- Detect skills with conflicting tool usage
- Identify resource contention (browser, file locks)
- Suggest skill compatibility matrix

### 6. Add Performance Profiling
- Track skill execution time over sessions
- Monitor API usage and costs
- Identify bottlenecks in skill chains

### 7. Create Skill Reputation System
- Track skill reliability across users
- Aggregate success/failure rates
- Community-rated skill quality scores

### 8. Implement A/B Testing Framework
- Compare two skills for same task
- Measure which completes faster/better
- Data-driven skill selection

### 9. Add Skill Update Notifications
- Monitor skill updates in ClawHub
- Alert on breaking changes
- Suggest upgrade timing

### 10. Create Skill Usage Analytics
- Track which skills are used most frequently
- Identify skill chains and workflows
- Optimize skill loading order

---

## Notes

- This skill adapts EEAT from content/code evaluation to AI agent skill vetting
- Security is elevated to critical importance due to system-level access
- Utility is evaluated comparatively (skill vs. baseline), not absolutely
- Gating mechanisms ensure skills only activate when dependencies are met
- Community signals (downloads, stars, issues) inform Authority dimension
- Prompt quality in SKILL.md directly impacts skill behavior
- Skills with executable scripts require deeper security audit
- This framework is designed for OpenClaw's modular skill architecture
