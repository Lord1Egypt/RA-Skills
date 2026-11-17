# Script Interface Contracts — GKN-Phantom

This document defines the **interface contract** for every script in `scripts/`.
Each script is specified by:
  - **Function signature** — the importable function name and parameters
  - **Input JSON** — the exact shape of input data
  - **Output JSON** — the exact shape of output data
  - **Error states** — all possible error conditions and their representations

The agent MUST conform to these contracts when calling scripts. Scripts are
treated as typed interfaces, not as file references.

---

## utils.py

Shared utilities. Importable, no CLI.

### `load_json(source: str) -> Any`
- **Input**: `source` = file path OR `"-"` for stdin
- **Output**: parsed JSON object (any type)
- **Error states**:
  - `FileNotFoundError` — file does not exist
  - `json.JSONDecodeError` — invalid JSON
  - `UnicodeDecodeError` — non-UTF-8 content (auto-wrapped to UTF-8)

### `dump_json(obj: Any, indent: int = 2) -> str`
- **Input**: any JSON-serializable object
- **Output**: UTF-8 JSON string (`ensure_ascii=False`)
- **Error states**: `TypeError` — object not serializable

### `resolve_ips(host: str, timeout: float = 3.0) -> list[str]`
- **Input**: hostname string
- **Output**: list of IP address strings (empty on failure)
- **Error states**: returns `[]` on DNS failure/timeout (never raises)
- **Side effect**: caches results per-run (call `clear_dns_cache()` to reset)

### `finding_fingerprint(finding: dict) -> str`
- **Input**: Finding dict (needs `type`, `target`, `evidence.request`)
- **Output**: 16-char SHA256 hex string
- **Error states**: never raises (handles missing fields gracefully)

### `dedup_against_memory(findings: list, prior: list) -> tuple[list, list]`
- **Input**: current findings + prior findings (from memory)
- **Output**: `(new_findings, known_findings)` — split by fingerprint match
- **Error states**: never raises (handles empty/null inputs)

---

## scope_guard.py

### `check_target(target: str, scope: dict) -> tuple[bool, str]`
- **Input**: target URL string + scope dict (`domains`, `ip_ranges`, `allowed_paths`, `blocked_paths`)
- **Output**: `(in_scope: bool, reason: str)` — reason empty when in_scope=True
- **Error states**:
  - `(False, "host 'X' does not match any scope domain")` — domain mismatch
  - `(False, "could not resolve host 'X'")` — DNS failure
  - `(False, "host 'X' (IP) not in any scope ip range")` — IP out of range
  - `(False, "path 'X' rejected by allowed/blocked path lists")` — path violation

### `run(targets: list[str], scope: dict) -> tuple[bool, list[str]]`
- **Input**: list of target URLs + scope dict
- **Output**: `(all_ok: bool, offenders: list[str])` — offenders is empty when all_ok=True
- **Error states**: none (returns offender list)

### CLI: `--context <path|-> [--url <url>]`
- **Exit 0**: all targets in scope
- **Exit 1**: one or more out of scope (offenders printed to stderr as JSON)
- **Exit 2**: input error (missing scope, no targets, invalid JSON)

---

## rate_limiter.py

### `RateLimiter(rps: float = 3.0, burst: int = 5, max_queue: int = 100)`
- **Input**: rps (requests/sec), burst (max tokens), max_queue (wait limit)
- **Output**: instance with `.acquire(timeout=None) -> float` method
- **`acquire()` return**: wait time in seconds (0.0 if granted immediately)
- **Error states**:
  - `QueueFullError` — wait queue full (caller should log + skip, never crash)
  - `TimeoutError` — timeout exceeded (caller should log + skip)
  - `ValueError` — invalid rps/burst (rps<=0 or burst<1)

---

## vuln_detector.py

### `build_plan(assets: dict, tiers: list, safe_mode: bool = True, include_l4: bool = False) -> list[dict]`
- **Input**:
  ```json
  {"endpoints": [{"url": "https://...", "methods": [...]}], "domains": [...], "ips": [...]}
  ```
- **Output**: ordered list of candidate Finding dicts (status="detected", confidence=0.5)
- **Error states**: returns empty plan if no endpoints or all tiers filtered out

### `classify_data_exposure(response_body: str) -> tuple[bool, int]`
- **Input**: HTTP response body string
- **Output**: `(triggered: bool, score: int)` — score >= 3 means triggered
- **Error states**: returns `(False, 0)` on empty/null input

### CLI: `--assets <path|-> --tier <all|low,medium,...> [--safe-mode|--no-safe-mode] [--include-l4]`
- **Exit 0**: plan generated (printed as JSON)
- **Exit 2**: invalid tier specified

---

## finding_validator.py

### `validate(finding: dict, replay_result: dict) -> dict`
- **Input**:
  ```json
  // finding: candidate Finding dict
  // replay_result:
  {"request": "...", "response": "...", "tool": "httpRequest", "signal_matched": true}
  ```
- **Output**: updated Finding dict with `status` = "validated" | "false_positive"
- **Error states**:
  - `status="false_positive"`, `validation_note="evidence incomplete; auto-FP"` — missing request/response/tool
  - `status="false_positive"`, `validation_note="signal not matched on replay"` — signal didn't reproduce
  - `status="false_positive"`, `validation_note="confidence X < 0.8"` — below threshold

### CLI: `--finding <path|-> --replay <path|->`
- **Exit 0**: finding validated (TP)
- **Exit 1**: finding is false positive (FP)

---

## attack_path.py

### `build_paths(findings: list[dict], assets: dict) -> list[dict]`
- **Input**: list of Finding dicts (only `status="validated"` are chained) + assets dict
- **Output**: list of AttackPath dicts (`{id, name, nodes, edges, impact, confidence}`)
- **Error states**: returns empty list if no validated findings
- **Edge relations**: `enables`, `enables_recon`, `escalates_to`, `exposes`, `co_located_weakness`

### CLI: `--findings <path|-> --assets <path|->`
- **Exit 0**: paths built (printed as JSON)

---

## report_generator.py

### `build_report(findings: list, assets: dict, paths: list, execution_log: list, blocked_l4: bool = False) -> dict`
- **Input**: validated findings + assets + attack paths + execution log + L4-blocked flag
- **Output**: FinalOutput dict (`{summary, risk_score, assets, findings, attack_paths, recommendations, sarif, execution_log}`)
- **Error states**: returns empty report if all inputs empty

### CLI: `--findings <path> --assets <path> --paths <path> --log <path> [--blocked-l4]`
- **Exit 0**: report generated (printed as JSON)

---

## state.py

### `StateSerializer(path: str)`
- **Methods**:
  - `checkpoint(current: str, history: list, context: dict = None) -> None` — atomic write
  - `load() -> dict` — load checkpoint
  - `exists() -> bool`
  - `clear() -> None`
- **Error states**:
  - `ValueError` — unknown state name in checkpoint()
  - `FileNotFoundError` — load() on non-existent file
  - `OSError` — write failure (falls back to shutil.move for cross-device)

### `next_state(current: str) -> str | None`
- **Input**: current state name
- **Output**: next state name, or `None` if current is DONE
- **Error states**: `ValueError` — unknown state

### `can_resume(checkpoint: dict) -> tuple[bool, str]`
- **Input**: loaded checkpoint dict
- **Output**: `(resumable: bool, current_state: str)` — str is reason if not resumable
- **Error states**: `(False, "invalid state 'X'")` or `(False, "run already completed")`

---

## adaptive_engine.py

### `detect_waf(result: dict) -> tuple[bool, str | None]`
- **Input**: HTTP result dict (`{status_code, headers, body}`)
- **Output**: `(waf_detected: bool, waf_type: str | None)` — waf_type is "cloudflare"|"akamai"|"mod_security"|"safedog"|"yundun"|"generic"|None
- **Error states**: returns `(False, None)` on empty result

### `generate_mutations(vuln_type: str, original_payload: str, max_variants: int = 5) -> list[str]`
- **Input**: vulnerability type + original payload string
- **Output**: list of mutated payload strings (up to max_variants)
- **Error states**: returns `[]` if no mutation strategy for this vuln_type

### `build_adaptive_plan(probe: dict, result: dict, vuln_type: str, original_payload: str, attempt: int = 1, max_retries: int = 3) -> dict`
- **Input**: original probe + failed HTTP result + vuln type + payload + attempt number
- **Output**:
  ```json
  {
    "action": "retry | mutate | fallback_signal | waf_bypass | abort",
    "reason": "...",
    "waf_detected": false,
    "waf_type": null,
    "retry_schedule": [{"attempt": 1, "delay_ms": 500}],
    "mutated_payloads": [],
    "alternative_signals": [],
    "fallback_strategy": null,
    "max_retries": 3,
    "attempt": 1,
    "failure_type": "transient | waf_blocked | false_negative | auth_required | not_found | server_error"
  }
  ```
- **Error states**: `action="abort"` with reason for unclassifiable failures

### CLI: `--probe <path|-> --result <path|-> --vuln-type <type> [--payload <str>] [--attempt N] [--max-retries N]`
- **Exit 0**: adaptive plan generated (action != abort)
- **Exit 1**: action=abort (no recovery possible)

---

## safety_simulator.py

### `score_target(target: str, recon_data: dict, config: dict) -> TargetRiskScore`
- **Input**: target URL + partial recon data (ports, endpoints, technologies) + config
- **Output**: `TargetRiskScore` with `score` (0-100), `risk_level`, `factors`, `recommendation`
- **Recommendation values**: `"scan"` | `"scan_narrowed"` | `"dry_run"` | `"require_approval"`
- **Error states**: never raises (defaults to low risk on missing data)

### `narrow_scope(scope: dict, risk_scores: list) -> dict`
- **Input**: original scope dict + list of TargetRiskScore dicts
- **Output**: narrowed scope dict (adds dangerous paths to `blocked_paths`)
- **Error states**: returns original scope if no critical-risk targets

### `dry_run(ctx: dict, plan: list) -> dict`
- **Input**: AgentContext + detection plan from vuln_detector
- **Output**:
  ```json
  {
    "mode": "dry_run",
    "total_probes": 88,
    "active_probes": 80,
    "blocked_probes": 8,
    "probes_needing_approval": 5,
    "l4_probes": 8,
    "by_tier": {"low": 20, "medium": 30, "high": 25, "critical": 13},
    "by_type": {"sqli": 4, "xss": 4, ...},
    "estimated_runtime_seconds": 35.2,
    "safe_mode": true,
    "safety_verdict": "SAFE_TO_PROCEED | REQUIRES_HUMAN_APPROVAL | CAUTION",
    "network_calls_made": 0
  }
  ```
- **Error states**: returns zero-probe report if plan is empty

### CLI: `--context <path|-> --mode <dry-run|risk-score|narrow-scope> [--plan <path>] [--recon <path>]`
- **Exit 0**: simulation complete
- **Exit 2**: missing required argument (e.g., --plan for dry-run)

---

## confidence_scoring.py

### `compute_confidence(finding: dict) -> ConfidenceBreakdown`
- **Input**: Finding dict (with evidence, replay_results, type, etc.)
- **Output**:
  ```json
  {
    "evidence_strength": 0.83,     // 0.0-1.0 (weight: 0.30)
    "reproducibility_score": 1.0,  // 0.0-1.0 (weight: 0.30)
    "signal_clarity": 0.98,        // 0.0-1.0 (weight: 0.25)
    "corroboration": 0.40,         // 0.0-1.0 (weight: 0.15)
    "confidence": 0.85,            // weighted aggregate 0.0-1.0
    "method": "weighted_v2",
    "meets_threshold": true         // confidence >= 0.80
  }
  ```
- **Scoring factors**:
  - `evidence_strength`: core fields present (50%) + status_code (15%) + response_time (10%) + body substance (15%) + headers (10%)
  - `reproducibility_score`: matched replays / total replays (or 0.5 for single confirmation)
  - `signal_clarity`: baseline per vuln type + safe_poc boost + descriptive signal boost
  - `corroboration`: multi-replay match (40%) + mutations tried (20%) + WAF detected (20%) + fallback used (10%) + fingerprint (10%)
- **Error states**: never raises (defaults to 0.0 scores on missing fields)

### `apply_confidence(finding: dict) -> dict`
- **Input**: Finding dict
- **Output**: updated Finding dict with `confidence`, `confidence_breakdown`, `reproducibility_score`, `meets_confidence_threshold` populated
- **Error states**: never raises (returns original finding on error)

### CLI: `--finding <path|->`
- **Exit 0**: confidence computed (printed as JSON)

---

## Integration: How scripts compose in the state machine

```
SCOPE_CHECK
  └─ scope_guard.run(targets, scope) → (ok, offenders)

[pre-flight] ← NEW: safety_simulator
  ├─ safety_simulator.dry_run(ctx, plan) → verdict
  ├─ safety_simulator.score_target(...) → risk per target
  └─ safety_simulator.narrow_scope(scope, scores) → narrowed scope

RECONNAISSANCE
  └─ utils.resolve_ips(host) → IPs

ACTIVE_TESTING
  ├─ vuln_detector.build_plan(assets, tiers) → candidate plan
  ├─ rate_limiter.acquire() → gate each probe
  ├─ [on failure] adaptive_engine.build_adaptive_plan(...) → retry/mutate/fallback  ← NEW
  └─ [per finding] confidence_scoring.apply_confidence(finding) → scored finding   ← NEW

VALIDATION
  ├─ finding_validator.validate(finding, replay) → validated/FP
  └─ confidence_scoring.compute_confidence(finding) → final confidence              ← NEW

ATTACK_PATH_ANALYSIS
  └─ attack_path.build_paths(findings, assets) → paths

REPORT_GENERATION
  └─ report_generator.build_report(...) → FinalOutput

[persistent]
  └─ state.StateSerializer → checkpoint/resume
```

---

## Quick Combat Pipeline modules (v5.4)

The one-command combat pipeline (`quick_combat.py`) and its helper modules.

### quick_combat.py — `run_combat_pipeline(...)`

```python
run_combat_pipeline(
    targets: list[str],                 # target URLs
    tech_data: dict | None = None,      # tech_fingerprint output
    output_dir: str = "./combat_output",
    use_nuclei: bool = True,
    quick_probes: bool = True,
    severity_filter: list[str] | None = None,
    rate_limit: int = 150,
    concurrency: int = 25,
    poc_formats: list[str] | None = None,
    deep: bool = True,                  # enables all layered extensions
    oob_client=None,                    # oob_client.OOBClient | None (C5)
    use_cn_probes: bool = True,         # domestic OA/component probes
    use_crawl: bool = True,             # katana full-site crawl (C3)
    use_js: bool = True,                # JS bundle mining (C4)
    use_memory: bool = True,            # cross-run dedup memory (C6)
) -> dict
```

- **Output**: manifest dict (pipeline_version "5.4.0", by_severity,
  duplicate_known, layers{cn_probes,katana_crawl,js_mining,oob_provider,
  memory_dedup}, artifacts{findings,pocs,exploits,index,combat_memory}, summary)
- **Error states**: every optional layer degrades to a no-op (missing katana /
  OOB provider / JS files) and logs into `summary` — the pipeline never aborts
- **Side effects**: writes `<output_dir>/<ts>/` artifacts and
  `<output_dir>/combat_memory.json` (when use_memory=True)

New pipeline phases (all gated by `deep=True`):

| Phase | Layer | What it does |
|-------|-------|--------------|
| 2.55  | CN probes | `cn_probes.probe_cn_components(targets)` — domestic OA fingerprints + one-shot verifiers |
| 2.6   | C3 crawl | `detect_katana()` → `crawl_katana()` → crawled parameterized URLs merge into `discover_params(extra_urls=...)` |
| 2.6   | C4 JS | `collect_js_urls()` + `analyze_target_js()` → JS findings + hidden endpoints fed to `probe_injection()` |
| 2.6   | C5 fire | `probe_blind_ssrf(target, entries, oob_client)` → OOB-tagged callbacks into `url`-style params |
| 3     | C5 verify | `verify_oob_pending(all_findings, pending, oob_client)` → validated blind-SSRF findings |
| 3.5   | C6 memory | `apply_memory_dedup()` marks known findings `[已提交]/[重复]`, then `merge_combat_memory()` persists |

CLI switches (v5.4): `--oob-provider {auto,interactsh,ceye,dnslog,none}`,
`--ceye-identifier`, `--ceye-token`, `--interactsh-server`,
`--no-cn-probes`, `--no-crawl`, `--no-js`, `--no-memory`.

### cn_probes.py — domestic OA/component unauthorized-access library

- **`CN_PROBES`** — list of 32 probe dicts, same shape as
  `quick_combat.QUICK_PROBES` plus optional `severity`, `method=POST` +
  `post_body` + `post_content_type` (one-shot verifiers), and `not_patterns`
  (soft-404 blacklist). Covers: 泛微 e-cology/e-office (BeanShell, Ssologin,
  /services/), 致远 seeyon (getSessionList, htmlofficeservlet,
  wpsAssistServlet), 通达 OA (/ispirit/, /module/), 用友 NC
  (~ic servlets, uapws), 禅道 (getconfig), JeecgBoot (jmreport
  queryFieldBySql one-shot SQLi verify, /sys/), 若依 RuoYi (druid
  prod-api/dev-api variants, /system/), 帆软 FineReport, 亿邮, 金蝶,
  蓝凌, 红帆, 万户.
- **`probe_cn_components(targets: list[str]) -> list[dict]`** — runs every
  probe via `quick_combat._run_quick_probe` (lazy import, no circular dep);
  per-probe errors are swallowed. Returns standard finding dicts.
- **CLI**: `--targets <csv|file|json>` → findings JSON on stdout, exit 2 on
  no targets.
- **Error states**: unreachable targets → `[]`, never raises.

### oob_client.py — real OOB callback channel

- **`get_oob_client(provider="auto", ceye_identifier=None, ceye_token=None,
  interactsh_server=None, startup_timeout=15.0) -> OOBClient | None`**
  - `provider="auto"` (default): interactsh binary in PATH → ceye env vars
    (`GKN_CEYE_IDENTIFIER` + `GKN_CEYE_TOKEN`) → None
  - explicit `interactsh` / `ceye` / `dnslog` skip auto-detection
  - `none`/`off` → None; any provider failure → None (never raises)
- **`OOBClient` interface**:
  - `get_domain(tag="gkn") -> str | None` — unique tagged callback domain
    (`{tag}.{correlation}.oast.fun` for interactsh; `{tag}.{id}.ceye.io`
    for ceye; `{tag}.{session}.dnslog.cn` for dnslog)
  - `poll(tag=None, wait=4.0) -> list[dict]` — interactions (optionally
    filtered by tag, blocking up to `wait`); `[]` on no match, never raises
  - `to_dict() -> dict` — serializable session state (no secrets)
  - `close()` — release the provider subprocess/session
- **CLI**: `--provider ... --tag gkn --wait 5` self-test; exit 1 when no
  provider is usable.
- **Error states**: unreachable APIs / dead subprocess → empty results, never
  raises.

### js_analyzer.py — new function (v5.4)

- **`extract_endpoint_entries(source: str, base_url: str = "",
  max_entries: int = 10) -> list[dict]`**
  - **Input**: JS source text + the page origin to resolve relative paths
  - **Output**: `[{"url": "https://origin/api/x?id=1", "param": "id",
    "value": "1"}]` — discover_params-compatible entries for
    `quick_combat.probe_injection()`. Only relative paths carrying a query
    string are extracted (hardcoded hidden API endpoints).
  - **Error states**: never raises; returns `[]` on no match.
