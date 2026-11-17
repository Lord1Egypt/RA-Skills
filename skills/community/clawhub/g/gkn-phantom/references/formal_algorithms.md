# Explainable Scoring Rules — GKN-Phantom v2.2

> **Documentation only.** This document describes the scoring and decision
> rules in plain language. It is a reference for auditors and integrators,
> not a normative mathematical specification. The implementation is in
> `scripts/decision_engine.py` (heuristic rules), `scripts/confidence_scoring.py`
> (weighted confidence), and `scripts/safety_simulator.py` (risk scoring).

---

## 1. Risk Scoring (Pre-Flight)

### 1.1 Target Risk Score

Each target receives a score 0–100 based on four additive factors:

| Factor | Max Contribution | Description |
|--------|-----------------|-------------|
| **Environment** | 20 | production=20, staging=10, dev=5, internal=0, lab=0 |
| **Port Exposure** | 30 | Each risky open port adds points (22: +10, 3306: +8, 6379: +8, 27017: +8, etc.) |
| **Path Sensitivity** | 30 | Endpoints matching sensitive paths (/admin, /actuator, /swagger, etc.) add points |
| **Tech Risk** | 25 | Risky technology fingerprints (Struts, ThinkPHP, Fastjson, etc.) add points |

Risk classification:

| Score Range | Risk Level | Recommendation |
|-------------|-----------|----------------|
| < 30 | low | Full scan |
| 30–59 | medium | Scan, narrowed scope |
| 60–79 | high | Dry-run first, then scan |
| ≥ 80 | critical | Require human approval, block dangerous paths |

### 1.2 Run Risk Score (Aggregate)

After validation, aggregate risk from findings:

| Severity | Points per finding |
|----------|-------------------|
| critical | 25 |
| high | 15 |
| medium | 8 |
| low | 3 |

Additional +5 if L4 was blocked (indicating potentially undiscovered critical findings).

### 1.3 Attack Path Risk

Each confirmed attack chain adds its cumulative severity points + 10 per additional hop beyond the first.

---

## 2. Scope Matching Rules

### 2.1 Domain Match

- **Exact**: `host == domain` → in scope
- **Wildcard** (`*.example.com`): `host ends with ".example.com"` OR `host == "example.com"` → in scope
- Otherwise → out of scope

### 2.2 IP Range Match

- Resolve the host to IP addresses (3s timeout, cached per run)
- If any resolved IP falls within any scope CIDR range → in scope

### 2.3 Path Match

- If `allowed_paths` is empty → all paths allowed
- Path must match at least one allowed prefix (or be `/`)
- Path must NOT match any blocked prefix
- Path match uses prefix semantics: `/api/` matches `/api/v1/users`

### 2.4 Composite Check

A target is in-scope only if domain AND IP AND path all pass.

---

## 3. Confidence Scoring

### 3.1 Four-Factor Weighted Score

| Factor | Weight | How It's Computed |
|--------|--------|-------------------|
| **Evidence Completeness** | 0.35 | Count of present core fields (request, response, timestamp, tool) ÷ 4 |
| **Reproducibility** | 0.35 | Fraction of replays where signal matched; 0.5 for single confirmation; 0.0 for none |
| **Signal Clarity** | 0.20 | Per-type baseline (e.g., sqli=0.90, logic_flaw=0.65) + 0.05 if safe_poc present |
| **Corroboration** | 0.10 | Multi-source agreement: +0.5 if ≥2 replays all matched, +0.3 if WAF detected, +0.2 if mutations tried |

Threshold: **0.80** → promoted to "validated".

### 3.2 Promotion Decision

A finding is promoted from "detected" to "validated" when ALL three hold:
1. Reproducible (signal matched on at least one replay)
2. Safe PoC (no destructive payload)
3. Confidence ≥ 0.80

---

## 4. Adaptive Engine Rules

### 4.1 Failure Classification

| Condition | Failure Type |
|-----------|-------------|
| timeout / connection_refused / connection_reset | transient |
| 403/406/429 + WAF header/body detected | waf_blocked |
| 200-299 + signal not matched | false_negative |
| 401/403 + no WAF detected | auth_required |
| 404/410 | not_found |
| 500-599 | server_error |

### 4.2 Adaptive Action Selection

| Failure Type | Attempt | Action |
|-------------|---------|--------|
| transient | < max_retries | retry with backoff |
| waf_blocked | mutations available | mutate payload |
| waf_blocked | no mutations left | fallback to alternative signal |
| false_negative | alt signals available | try alternative signal |
| server_error | < 2 attempts | retry |
| any | exhausted | abort |

### 4.3 Retry Backoff Schedule

| Attempt | Delay |
|---------|-------|
| 1 | 500ms |
| 2 | 1000ms |
| 3 | 2000ms |
| 4 | 4000ms |
| 5 | 8000ms (capped) |

---

## 5. Heuristic Decision Rules (v2.2 REPLACES probabilistic v2.1)

> **v2.2 CHANGE**: The sigmoid/Bayesian probabilistic layer from v2.1 has been
> replaced with deterministic heuristic scoring + rule fallback. All decisions
> are now 100% reproducible — same input always produces the same output.

### 5.1 Probe Continuation

Rules evaluated in order, **first match wins**:

| Rule | Condition | Decision |
|------|-----------|----------|
| A | probes_executed ≥ budget | STOP (budget exhausted) |
| B | no findings AND >20% budget used | STOP (low yield) |
| C | discovery_yield ≥ 0.05 | CONTINUE (still finding vulns) |
| D | >50% budget remaining AND <20 probes | CONTINUE (early stage) |
| E | otherwise | STOP (diminishing returns) |

Where `discovery_yield = validated_count / probes_executed`.

### 5.2 Severity Upgrade

Additive scoring (not sigmoid):

| Factor | Points | Condition |
|--------|--------|-----------|
| Exposes PII | +3.0 | email/phone/SSN/password/secret/api_key/token in response |
| Cross-user impact | +2.5 | IDOR or stored XSS on high-severity finding |
| Corroboration | +2.0 | corroboration ≥ 0.5 (multi-source agreement) |
| Reproducibility | +1.5 | reproducibility ≥ 0.8 |

- **score ≥ 2.5** → UPGRADE one severity level
- **score < 2.5** → KEEP current severity

### 5.3 Scope Expansion

Sequential gates (not probability thresholds):

| Gate | Condition | Result |
|------|-----------|--------|
| 1 | candidate is production | BLOCK (never expand) |
| 2 | candidate risk_score ≥ 80 | BLOCK (too dangerous) |
| 3 | chain_potential < 0.5 | KEEP (not enough value) |
| 4 | no validated findings | KEEP (nothing to chain from) |
| 5 | all gates passed | PROPOSE EXPANSION (needs human approval) |

Chain potential assessment (deterministic):

| Evidence | Contribution |
|----------|-------------|
| component_exposure finding exists | 0.7 |
| weak_credential finding exists | 0.6 |
| candidate is on same host as existing finding | 0.5 |
| any high/critical finding exists | 0.3 |

Capped at 1.0.

### 5.4 Finding Confidence (Heuristic, replaces Bayesian)

Same four-factor weighted formula as §3.1, but computed with fixed weights
and deterministic per-type signal clarity baselines. No Bayesian prior or
posterior — the score is an additive weighted sum.

---

## 6. State Recovery Rules

### 6.1 Checkpoint Validity

A checkpoint is resumable when:
- `current` is a valid state (not DONE)
- `history` is non-empty
- `context_snapshot` contains `scope` and `targets`
- `checkpointed_at` is a valid ISO 8601 timestamp

### 6.2 Resume Strategy

- If `partial_results` exists → skip already-probed endpoints, replay from current state
- Otherwise → restart the state from scratch

### 6.3 Failure Rollback

On catastrophic failure (all retries exhausted):
1. Restore context snapshot to previous safe state
2. Append rollback event to history
3. Mark current = previous state
4. Re-attempt with degraded strategy (reduced tier, skipped probe)

Safe rollback states: INIT, SCOPE_CHECK, PRE_FLIGHT, RECONNAISSANCE.

---

## References

- `scripts/confidence_scoring.py` — implements §3
- `scripts/safety_simulator.py` — implements §1.1, §1.3, §2.5
- `scripts/scope_guard.py` — implements §2.1–2.4
- `scripts/adaptive_engine.py` — implements §4
- `scripts/decision_engine.py` — implements §5 (v2.2 heuristic, replaces v2.1 probabilistic)
- `scripts/state_recovery.py` — implements §6
- `scripts/report_generator.py` — implements §1.2
