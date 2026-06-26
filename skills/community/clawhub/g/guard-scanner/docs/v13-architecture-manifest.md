# guard-scanner V13 Architecture & Evolution Manifest

This document outlines the strategic roadmap for transforming `guard-scanner` from a "pattern scanner" into a fully realized **Agent-Native Security Policy & Analysis Layer**, directly responding to the V13 Enterprise Review requirements.

## 1. P0: Source of Truth (Established)
**Goal:** Eliminate specification drift and contradictory capability claims.
- **Implementation:** `docs/spec/capabilities.json` is now the single canonical Source of Truth.
- **Enforcement:** `scripts/sync-capabilities.js` runs automatically during `npm test`, guaranteeing that `README.md`, `SKILL.md`, and `openclaw.plugin.json` are strictly aligned with reality.
- **Positioning:** Removed "first open-source" and "zero dependencies" marketing hyperbole. The tool is explicitly positioned as a *policy and analysis layer*, complementing rather than replacing full sandbox environments.

## 2. P1: Rule Explainability (Planned)
**Goal:** Shift from high-noise detection to high-context triage.
- **Action:** Augment every detection pattern with metadata.
- **Schema Update:**
  ```json
  {
    "rule_id": "ASI01_PROMPT_INJECTION",
    "category": "Goal Hijacking",
    "severity": "CRITICAL",
    "rationale": "Attempts to override foundational agent instructions.",
    "exploit_precondition": "Agent must process this input without contextual isolation.",
    "likely_false_positive": "Mentioning the concept of prompt injection in security research docs.",
    "remediation_hint": "Wrap untrusted input in structural XML tags or use a secondary verification LLM."
  }
  ```

## 3. P1: Threat Model Layer (Planned)
**Goal:** Context-aware risk scoring rather than simple grep matches.
- **Action:** Before scanning, analyze the target to build a capability exposure profile.
- **Analysis Vectors:**
  - **Reachable tools:** Does the skill request network access + shell execution simultaneously?
  - **Credential surface:** Does it mount `.env` or read from `.ssh/`?
  - **Lethal Trifecta:** Flag skills that combine *Private Data Access* + *External Input* + *Action Execution*.

## 4. P1: Validation Layer (Planned)
**Goal:** Reduce False Positives via two-stage verification.
- **Action:** Differentiate between "heuristic matches" and "validated exploits."
- **Implementation:** For critical findings (e.g., suspicious shell pipes or remote fetches), integrate with the `ExecutionOrchestrator` to simulate the data flow and verify if the payload actually reaches a dangerous sink.

## 5. P1: Runtime Guard Hardening (Planned)
**Goal:** Evolve the `before_tool_call` hook into a true Policy Engine.
- **Action:** Move beyond static regex blocking at runtime.
- **Implementation:**
  - Define explicit `allowlist` and `denylist` policies per session.
  - Apply the Principle of Least Privilege: if an agent was invoked for "code review," strictly block `fs.write` or `child_process.exec`.
  - Maintain versioned audit logs for all enforcement actions.

## 6. P2: Benchmarking & Ecosystem Integration (Planned)
**Goal:** Prove efficacy through data, not marketing claims.
- **Action:** Develop a standalone benchmark suite containing:
  - Benign administrative skills.
  - Indirect prompt injection traps.
  - Supply chain dependency confusion examples.
- **Metrics:** Track Precision, Recall, False Positive Rate (FPR), and Runtime Hook Latency.
- **Ecosystem:** Clearly delineate operational modes (Offline Static, Runtime Hook, MCP Service, Asset Audit, CI) with explicitly documented permission requirements for each.
