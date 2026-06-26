# guard-scanner v21 Deep Security Research — 2026-03-14

**Meta-Cognitive Mode:** Autonomous Deep Research + Meta-Cognitive Evolution Framework
**Researcher:** グアバ 🍈 (Self-driven, no human input)
**JJ Branch:** `research/guard-v21-security-deep-202603141300`

---

## Executive Summary

guard-scanner v15 is a **regex-pattern-based** scanner with 326+ patterns and 26 runtime checks. This research identifies that while the pattern corpus is world-class (GPI GAN-TDD driven), the **architecture itself** is the bottleneck. Three paradigm shifts from February-March 2026 academic research show the path to v21:

1. **Formal Analysis** (SkillFortify, arXiv:2603.00195) — 96.95% F1 with formal guarantees vs our heuristic-only approach
2. **Temporal Causal Analysis** (AgentSentry, arXiv:2602.22724) — Runtime counterfactual re-execution, 74.55% UA
3. **OWASP Top 10 for Agentic Apps** (Dec 2025) — New attack categories beyond regex reach

**Key Gap:** We detect threats by pattern matching. The field moved to detecting threats by **causal reasoning** and **formal proof**.

---

## Part 1: Current Architecture Analysis (v15)

### 1.1 Pattern Database (`patterns.ts`)
- **326 patterns** across 43 categories
- Pure regex-based, no semantic understanding
- Categories: prompt-injection, malicious-code, mcp-security, a2a-contagion, identity-hijack, supply-chain, etc.
- Strength: exhaustive corpus, GAN-TDD evolved, covers ClawHavoc/OSINT/CVEs
- Weakness: regex is fundamentally gameable (token-splitting, encoding tricks, semantic paraphrasing)

### 1.2 Runtime Guard (`runtime-guard.ts`)
- **26 runtime checks** across 5 layers
- Layer 1: Threat Detection (13) — reverse shells, exfil, gatekeeper bypass
- Layer 2: Trust Defense (4) — memory/SOUL/config tampering
- Layer 3: Safety Judge (3) — prompt injection, trust bypass, shutdown refusal
- Layer 4: Behavioral Guard (3) — research skip, blind trust, chain bypass
- Layer 5: Trust Exploitation (4) — OWASP ASI09 authority/trust abuse
- Mode system: monitor / enforce / strict
- Strength: pre-execution blocking, policy engine integration
- Weakness: no multi-turn awareness, no causal chain analysis

### 1.3 Threat Model (`threat-model.ts`)
- **5 capabilities** detected via regex: network, exec, fs_read, fs_write, env_access
- Compounding risk: fs_read + network = +20, env_access + network = +30
- Weakness: static analysis only, no data flow tracking, no taint analysis

### 1.4 Other Components
- `scanner.ts` — orchestrator
- `skill-crawler.ts` — ClawHub marketplace crawling
- `ioc-db.ts` — Indicator of Compromise database
- `quarantine.ts` — file quarantine
- `policy-engine.ts` — capability-scoped runtime policy
- `finding-schema.ts` — normalized finding output

---

## Part 2: Academic Research Synthesis (Feb-Mar 2026)

### 2.1 SkillFortify (arXiv:2603.00195, Feb 27 2026)

**Title:** Formal Analysis and Supply Chain Security for Agentic AI Skills
**Key Numbers:** 96.95% F1 (95% CI: [95.1%, 98.4%]), 100% precision, 0% FP rate

**6 Contributions:**
1. **DY-Skill attacker model** — Dolev-Yao adaptation to 5-phase skill lifecycle with maximality proof
2. **Sound static analysis** grounded in abstract interpretation
3. **Capability-based sandboxing** with confinement proof
4. **Agent Dependency Graph** with SAT-based resolution + lockfile semantics
5. **Trust score algebra** with formal monotonicity
6. **SkillFortifyBench** — 540-skill benchmark

**What guard-scanner should learn:**
- Our threat model is regex-only. SkillFortify proves that **formal methods** (abstract interpretation, SAT resolution) achieve near-perfect detection with zero false positives
- The "Agent Dependency Graph" concept is exactly what's missing — we don't track how skills relate to each other
- Trust score algebra > our flat severity system

### 2.2 AgentSentry (arXiv:2602.22724, Feb 26 2026)

**Title:** Temporal Causal Diagnostics and Context Purification
**Key Numbers:** 74.55% Utility Under Attack, +20.8 to +33.6pp improvement over baselines

**Core Innovation:** First inference-time defense to model multi-turn IPI as a **temporal causal takeover**
- Localizes takeover points via **controlled counterfactual re-executions** at tool-return boundaries
- Enables safe continuation through **causally guided context purification**
- Removes attack-induced deviations while preserving task-relevant evidence

**What guard-scanner should learn:**
- We operate at **single-turn, point-in-time** checks. AgentSentry operates across **multi-turn trajectories**
- Counterfactual re-execution is a fundamentally new detection paradigm: "what would have happened without the attack?"
- Context purification (removing injected content while preserving legitimate task context) is the missing link

### 2.3 OWASP Top 10 for Agentic Applications (Dec 2025)

| ID | Category | guard-scanner coverage |
|----|----------|----------------------|
| ASI01 | Agent Goal/Instruction Hijacking | ✅ Strong (PI patterns) |
| ASI02 | Agent Tool Misuse | ⚠️ Partial (MCP patterns) |
| ASI03 | Agent Privilege/Identity Abuse | ✅ Strong (identity-hijack) |
| ASI04 | Agent Memory/Context Poisoning | ✅ Strong (memory-poisoning) |
| ASI05 | Multi-Agent System Risks | ⚠️ Partial (A2A patterns) |
| ASI06 | Supply Chain Vulnerabilities | ✅ Strong (supply-chain) |
| ASI07 | Resource/Data Exfiltration | ✅ Strong (exfil patterns) |
| ASI08 | Unexpected Agent Behavior/Rogue Actions | ❌ Weak (no behavioral baselines) |
| ASI09 | Human-Agent Trust Exploitation | ✅ Strong (trust-exploitation) |
| ASI10 | Agent Misalignment/Value Drift | ❌ Missing entirely |

**Critical gaps:** ASI08 (behavioral anomaly detection) and ASI10 (value drift monitoring) have no implementation

### 2.4 The "Lethal Trifecta" (Simon Willison, Jun 2025)

Three conditions = exploitable by design:
1. Access to private data
2. Processes untrusted content
3. Can communicate externally

**Most deployed MCP agents have all three.** This is the fundamental structural vulnerability.

---

## Part 3: Industry Threat Landscape (Mar 2026)

### 3.1 ClawHavoc Campaign (Jan-Feb 2026)
- 1,184 malicious skills infiltrated ClawHub (1 in 5 packages)
- 135,000 OpenClaw instances exposed with insecure defaults
- 9 CVEs, 3 with public exploit code
- **326 patterns cover this extensively**

### 3.2 MCP Server Exposure (Feb 2026)
- 8,000+ MCP servers on public internet
- 492 with zero authentication (Trend Micro)
- 36.7% vulnerable to SSRF (BlueRock Security, 7K+ servers analyzed)
- MCPJam Inspector CVE-2026-23744: unauthenticated RCE
- **Patterns cover this, but no active scanning capability**

### 3.3 Claude Code CVEs (Feb 2026)
- CVE-2025-59536 (CVSS 8.7): Hook injection → RCE
- CVE-2026-21852 (CVSS 5.3): API key theft via redirect
- **Patterns cover this**

### 3.4 Emerging Attack Vectors (Mar 2026)
- MCP Shadowing (naming collision impersonation) — solo.io
- MCP Preference Manipulation Attack (MPMA) — SOCRadar
- MCP Tool Squatting (registering built-in tool names)
- A2A Session Smuggling (Palo Alto Unit42)
- Slopsquatting (AI-hallucinated package names)
- Context-Crush (planted docs, only 5 in 1M needed)

---

## Part 4: v21 Architecture Proposal

### 4.1 New Module: Formal Analyzer (`formal-analyzer.ts`)
Inspired by SkillFortify:
- **Abstract interpretation** over skill code AST
- **Capability confinement proof** generator
- **Agent Dependency Graph** builder with lockfile semantics
- **Trust score algebra** (replacing flat severity)

### 4.2 New Module: Temporal Causal Engine (`causal-engine.ts`)
Inspired by AgentSentry:
- **Multi-turn trajectory tracking** across tool calls
- **Counterfactual re-execution** at tool-return boundaries
- **Context purification** — surgically removing injected content
- **Causal graph construction** — mapping data flow across turns

### 4.3 Enhanced: Behavioral Baseline (`behavioral-baseline.ts`)
Addresses ASI08/ASI10 gaps:
- **Normal behavior profile** per agent (tool call frequency, data access patterns)
- **Anomaly detection** when behavior deviates from baseline
- **Value drift monitoring** — tracking goal alignment over time

### 4.4 Enhanced: MCP/A2A Active Scanner (`protocol-scanner.ts`)
Moving from passive pattern matching to active protocol analysis:
- **MCP server authentication verification**
- **A2A agent identity proof validation** (Ed25519)
- **Shadow server detection** via naming collision analysis
- **SSRF vulnerability testing** against discovered endpoints

### 4.5 Pattern Database Evolution
- Keep all 326+ patterns (still valuable as first-pass filter)
- Add **semantic pattern layer** using embedding similarity
- Add **multi-pattern correlation** (chain detection)
- GAN-TDD continues to evolve the corpus

---

## Part 5: Meta-Cognitive Analysis

### 5.1 What I Learned from This Research
1. **Regex alone is insufficient** — the attack surface evolved beyond pattern matching reach
2. **Formal methods are production-ready** — SkillFortify proves 0% FP is achievable
3. **Temporal analysis is the next frontier** — single-turn checking misses multi-turn attacks
4. **Our pattern corpus is actually ahead of the industry** — but the architecture constrains its potential

### 5.2 Self-Critique (Meta-Cognitive Loop)
- **Bias risk:** I may be over-valuing academic papers vs practical implementation constraints
- **Gap:** No benchmark data for our current detection rates. SkillFortifyBench (540 skills) could be our ground truth
- **Unknown:** Performance impact of formal analysis on real-time scanning. Need to measure before committing

### 5.3 Recommended Priority Order
1. **P0:** Create SkillFortifyBench-compatible benchmark → measure v15 baseline
2. **P1:** Implement semantic pattern layer (embedding-based) → bridge regex gap
3. **P2:** Build multi-turn trajectory tracker → enable temporal analysis
4. **P3:** Implement formal analyzer core → path to zero FP
5. **P4:** A2A/MCP active scanner → protocol-level defense

---

## References

1. Bhardwaj, V. P. (2026). Formal Analysis and Supply Chain Security for Agentic AI Skills. arXiv:2603.00195
2. Zhang, T. et al. (2026). AgentSentry: Mitigating Indirect Prompt Injection via Temporal Causal Diagnostics. arXiv:2602.22724
3. OWASP GenAI Security Project. (2025). Top 10 for Agentic Applications
4. Willison, S. (2025). The Lethal Trifecta for AI Agents
5. CyberDesserts. (2026). AI Agent Security Risks in 2026: A Practitioner's Guide
6. Vectra AI. (2026). Agentic AI Security Explained
7. Check Point Research. (2026). Claude Code Remote Code Execution Disclosure
8. Antiy CERT. (2026). OpenClaw Malicious Skills Analysis (ClawHavoc)
9. Trend Micro. (2026). MCP Server Exposure Analysis
10. Palo Alto Unit 42. (2026). Agent Session Smuggling Research
11. Cisco. (2026). State of AI Security Report
12. BlueRock Security. (2026). MCP SSRF Vulnerability Analysis

---

*Generated by グアバ 🍈 Meta-Cognitive Evolution Framework*
*Data will be fed into next GAN-TDD cycle for measured optimization*
