# Extending NOMOS into Enterprise Modules

> Companion to [`README-zh.md`](../README-zh.md). This guide describes the single
> extension point through which NOMOS serves enterprise management domains, and
> catalogues the module categories it can be extended into.

---

## 1. What "extending NOMOS" means

NOMOS is a deterministic decision kernel. It does not own your data, and it does
not replace the systems that do. Extending NOMOS into an enterprise module means
attaching **domain guardrails** to the decision pipeline — not moving business
logic into the engine.

The extension point is the **domain control pack** (`src/second_perspective/domain/`).

A pack encodes domain-specific policy: regulatory thresholds, mandatory
disclosures, hard constraints, required responsibility declarations. Packs sit
*outside* the deterministic core, and they observe only.

Three properties are structural, not stylistic:

1. **A pack never alters a verdict.** It cannot change a score, a ranking, a
   status, or an assumption state. The engine's result is out of its reach.
2. **A pack never invents missing data.** It may report that a required
   declaration is absent. It may not supply one.
3. **A pack must never crash the pipeline.** Its failures are contained.

Violations surface as `warning` or `error` records. When `fail_on_violation` is
enabled on the service, an `error` blocks sealing of the report; the decision
itself still has to be signed by a human.

---

## 2. The contract

A pack is any object satisfying this protocol:

```python
from dataclasses import dataclass
from typing import Protocol

from second_perspective.models.schemas import DecisionRequest


@dataclass
class DomainViolation:
    pack_id: str
    code: str
    message: str
    severity: str = "warning"      # "warning" | "error"


class DomainControlPack(Protocol):
    id: str
    description: str

    def validate(self, request: DecisionRequest) -> list[DomainViolation]: ...
```

`validate()` receives the full decision request and returns zero or more
violations. It is a pure observation: it reads the request, it does not write to
it.

---

## 3. Registering a pack

```python
from second_perspective.domain import get_registry

class ShiftRestPeriodPack:
    id = "workforce-shift-rest-period"
    description = (
        "Flags shift assignments that do not declare a minimum rest-period "
        "constraint."
    )

    def validate(self, request):
        violations = []
        try:
            if not getattr(request, "responsibility", None):
                violations.append(
                    DomainViolation(
                        pack_id=self.id,
                        code="NO_SHIFT_APPROVER",
                        message="Shift assignment declares no approving owner.",
                        severity="warning",
                    )
                )
        except Exception:
            return violations     # a pack must never crash the pipeline
        return violations


get_registry().register(ShiftRestPeriodPack())
```

Packs registered this way are evaluated on every request that flows through the
service. The shipped reference pack is registered by
`second_perspective.domain.register_default_packs()`.

---

## 4. Module catalogue

Two states are distinguished throughout. **Shipped** means the pack exists in
this repository today. **Extension target** means the module maps cleanly onto
the contract above but is not implemented here — building it is a pack, not a
change to the engine.

| # | Enterprise module | Decision class it feeds | What the pack observes | State |
|---|---|---|---|---|
| 1 | Workforce & shift scheduling | Shift assignment, overtime and substitution exceptions | Whether the assignment declares an approving owner and an explicit rest-period constraint; whether a substitution names the party it replaces | Extension target |
| 2 | Internal materials & document control | Release, revision and retention decisions on internal documents | Whether a document class and a retention owner are declared before release | Extension target |
| 3 | Finance & risk control | Multi-alternative capital and exposure decisions | Whether a multi-alternative decision declares an explicit risk owner | **Shipped** (`finance-risk-control`) |
| 4 | Procurement & supplier onboarding | Supplier admission, contract award, exception waivers | Whether the award declares the evaluation criteria and the awarding owner | Extension target |
| 5 | Compliance & regulatory reporting | Filing decisions and disclosure approvals | Whether each mandatory disclosure field is declared as present or explicitly absent | Extension target |
| 6 | Capital allocation & investment review | Portfolio and investment committee decisions | Whether scenario assumptions and their failure branches are declared | Extension target |
| 7 | Project & change approval | Gate reviews, change requests, rollbacks | Whether the rollback path and its trigger condition are declared | Extension target |
| 8 | Contract exception handling | Non-standard terms, price and term deviations | Whether the deviation names the party authorised to accept it | Extension target |
| 9 | Records retention & audit trails | Disposition and hold decisions | Whether the retention period and the hold owner are declared | Extension target |

Only module 3 ships with this repository. Every other row is a supported shape
for a domain control pack; none of them is claimed as a delivered feature.

---

## 5. How a module attaches to the pipeline

NOMOS does not pull data. An upstream system pushes a structured request:

```
Upstream system (any of the modules above)
    │  DecisionRequest + declared assumptions + declared interactions
    │  + declared responsibility
    ▼
POST /v1/decisions/evaluate      or      POST /v1/hub/analyze
    │
    ├── deterministic core: structure audit → constraints → scoring →
    │   first-order invalidation → second-order interaction → three-layer
    │   reconstruction → convergence classification → counterfactuals
    │
    ├── domain control packs  ← the extension point described here
    │       observe only; emit warnings / errors; never alter the verdict
    │
    └── sealed report + hash-chained audit trail
    ▼
Human approval
    │  the verdict stays outside the algorithm; a person signs it
    ▼
Downstream audit, approval and reporting flows
```

The pack layer is deliberately the narrowest part of that pipeline. Anything a
module needs to *decide* belongs upstream; anything it needs to *enforce* belongs
in a pack.

---

## 6. Boundaries

These hold for every module, shipped or not:

- The engine never estimates missing interaction strengths, weights,
  probabilities, or responsible parties.
- Packs observe; they never adjudicate, rank, score, or mutate the request.
- LLMs never adjudicate. The three-tier permission gate (annotation / proposal /
  narrative) applies to every module identically.
- The cognitive scanner challenges structural risk only. It does not diagnose
  people, read motives, or replace legal, medical, financial, or security
  professionals.
- A pack that raises `error` blocks report sealing; it does not publish a
  different verdict.

---

## 7. Adding a module, in order

1. Name the decision class the module feeds, and the domain policy it must enforce.
2. Write the policy as observations over a `DecisionRequest` — never as a
   computation that fills in what the request omits.
3. Implement `id`, `description`, and `validate()`.
4. Register it through `get_registry().register(...)`.
5. Decide whether its violations are `warning` or `error`, and whether the
   service runs with `fail_on_violation` enabled.
6. Record the module in this catalogue, with an honest state label.
