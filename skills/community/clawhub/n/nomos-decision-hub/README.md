<p align="center">
  <img src="https://img.shields.io/badge/python-3.11%2B-D4AF37?style=flat-square" alt="python">
  <img src="https://img.shields.io/badge/engine-v0.7.0-D4AF37?style=flat-square" alt="engine-v0.7.0">
  <img src="https://img.shields.io/badge/operators-10-D4AF37?style=flat-square" alt="operators-10">
</p>

<blockquote align="center">
  <em>NOMOS · v0.7.0</em>
</blockquote>

## About

NOMOS is a deterministic, auditable decision-orchestration engine with no probabilistic
black boxes. Every decision decomposes into a traceable causal topology, with
compliance-grade audit trails, declared scenario stress tests, and human-in-the-loop
governance.

It does not invent missing facts, weights, thresholds, owners, evidence, or
probabilities. It produces leading candidates under declared inputs and always keeps
final authority outside the algorithm.

For the full Chinese documentation see [`README-zh.md`](./README-zh.md).

## Version matrix

| Version | Adds |
| --- | --- |
| **0.7.0** | Meta-causal ledger terminology alignment (**breaking**): ASCII keys `trace_gap` / `parallel_convergence` / `narrative_occlusion` / `bounded_audit` / `causal_succession`; reason-code prefixes `TRACE_` / `CONVERGENCE_` / `NARRATIVE_` / `AUDIT_` / `SUCCESSION_`; no aliases kept |
| **0.6.0** | Cognitive audit kernel 5 → **10 operators**; topology substrate; META ledger (measure-only, never blocks); proposal-only evolution layer; `GCAE-1.0.0 → GCAE-1.1.0` |
| **0.5.0** | Enterprise control plane: event store, tenant isolation, OIDC + scopes, KMS signing, rate limiting, observability, migrations/backups, domain control packs (all env-gated, off by default) |
| **0.4.0** | Second-order causality: assumption interaction (I-1…I-4), formal convergence (5 states), LLM permission gate (T1/T2/T3) |
| **0.3.0** | `IntelligentDecisionHub`, sealed `HubReport`, `POST /v1/hub/analyze`, scenario stress tests, information priorities |

Full log: [`CHANGELOG.md`](./CHANGELOG.md).

## Ten-operator cognitive audit kernel

`ORI` origin anchor · `NS` narrative strip · `IAP` implicit assumption · `LCH` latch /
fragility · `TPG` rule-free thinking (topology) · `BFC` binary fact check · `CCS`
causal-chain sync · `GRF` gray feedback · `META` meta-causal ledger · `STATE` state
anchor.

The topology substrate runs four parallel checks: consistency · constraint · closure ·
**time order**. `ORI` and `GRF` register conditionally — only when an origin or a
gray-level ladder is declared — so no permanently-true blocker can be introduced.

## Install

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -e .
```

## Run demonstrations

```bash
nomos-demo                                          # core decision foundation
nomos-demo --decision examples/market_entry.json --json
nomos-hub-demo                                      # hub with two stress scenarios
```

## Python usage

```python
from second_perspective import IntelligentDecisionHub
from second_perspective.models import HubAnalysisRequest

request = HubAnalysisRequest.model_validate({
    "decision": decision_payload,
    "scenarios": [
        {"id": "SC1", "name": "Critical assumption fails",
         "failed_assumption_ids": ["A1"]},
        {"id": "SC2", "name": "Cost shock",
         "metric_overrides": {"S2": {"capital_required": 6000000}}},
    ],
})
report = IntelligentDecisionHub().analyze(request)
print(report.model_dump_json(indent=2))
```

## Run the API

Development may run without a key; production fails closed without one.

```bash
export SP_ENV=development
uvicorn second_perspective.api.main:app --reload
```

Endpoints: `POST /v1/hub/analyze`, `GET /v1/hub/reports/{hub_run_id}`,
`POST /v1/decisions/evaluate`, `GET /v1/decisions/{decision_id}`,
`GET /v1/decisions/{decision_id}/history`,
`POST /v1/decisions/{decision_id}/approval`, `GET /health`, `GET /v1/metrics`.

Protected clients send `Authorization: Bearer <SP_API_KEY>`.

## Docker

```bash
docker build -t nomos-hub .
docker run -p 8000:8000 \
  -e SP_ENV=production \
  -e SP_API_KEY=your-secret-key \
  -e SP_DATABASE_DSN=postgresql://user:pass@db:5432/nomos \
  nomos-hub
```

## Documentation

- [`docs/DECISION_FOUNDATION_V0_2.md`](docs/DECISION_FOUNDATION_V0_2.md) — the deterministic decision foundation and its invariants.
- [`docs/INTELLIGENT_DECISION_HUB_V0_4.md`](docs/INTELLIGENT_DECISION_HUB_V0_4.md) — second-order causality: interaction, convergence, LLM gate.
- [`docs/ENTERPRISE_MODULES.md`](docs/ENTERPRISE_MODULES.md) — domain control packs and enterprise extension points.
- [`docs/VERIFICATION_GUIDE.md`](docs/VERIFICATION_GUIDE.md) — verifying audit chains and sealed reports.
- [`docs/archive/`](docs/archive/) — historical v0.3 hub document.
- `scripts/export_openapi.py` regenerates the OpenAPI contract.

## Production boundary

The default repository is process-local memory. Production deployments need durable
event storage, OIDC and authorization enforcement, tenant isolation, KMS signatures,
rate limiting, observability, backups, and migrations — all shipped in v0.5 but
**env-gated and off by default**.

The cognitive scanner challenges structural risks. It does not diagnose people, read
motives, or replace legal, medical, financial, or safety professionals.

## License & Authorization

This repository is **not open-source** and **not MIT-0**. Dual-track model: free for
individual non-commercial research; paid commercial authorization required for
government / enterprise use. See [`LICENSE`](./LICENSE) — within the PRC the licensor
is Shanghai Linming Junhua Technology Co., Ltd.; outside the PRC it is NOHN AI
TECHNOLOGY PTE. LTD. (Singapore law, SIAC arbitration).
