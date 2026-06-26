# Sprint Contracts: Data Structures and Harness Enforcement

Sprint contracts live in `models/state.py` (written in Phase 1). This file covers:
- How to write contracts that the harness can enforce automatically
- The Generator system prompt section that injects contract awareness
- The interactive negotiation pattern vs. config-file pattern
- How to declare evidence surfaces so the Evaluator does not scatter files or guess probes

---

## The Core Rule: Criteria Must Be Behaviorally Testable

The Evaluator verifies success criteria from declared evidence: browser interaction, API calls,
commands, source excerpts, screenshots, or audit output. Every criterion must say how it can
be verified. UI criteria should be browser-observable; production/QA criteria may use command
or source evidence when behavior is not visible in the browser.

**Good (observable behavior):**
```
"Submitting the form with a valid email shows a success banner and the new item appears in the list."
"Reloading the page after creating an item still shows that item."
"Submitting with an empty required field shows an error message, not a crash."
```

**Bad (not observable without reading code):**
```
"The sendEmail function is implemented."
"The database schema has a users table."
"Error handling is in place."
```

---

## Generator System Prompt Section for Contract Awareness

Include this block in `harness/prompts/generator.md` (injected via the system array in
`agents/generator.py`, not hardcoded into the prompt file):

```
## Sprint Contract Enforcement

You are working on Sprint {sprint_number}: {goal}

SUCCESS CRITERIA (ALL must be verifiable by an Evaluator opening the app):
{success_criteria_list}

OUT OF SCOPE THIS SPRINT:
{out_of_scope_list}

EVIDENCE SURFACES:
{evidence_list}

Rules:
- Build ONLY what is in the sprint scope. Do not build ahead.
- Each success criterion must be demonstrable via browser interaction or API call.
- Do not create public evidence routes/files unless EVIDENCE SURFACES explicitly allows them.
- Commit after each feature unit (not after the whole sprint).
- When done, write a brief summary of what was built and any known issues.
```

Inject this dynamically in `run_generator()` by formatting the sprint contract fields
into the system messages list — see the `system` array construction in Phase 3.

---

## Agent-Negotiated Contracts (preferred for quality-focused harnesses)

**Root cause of original omission:** The skill assumed humans know success criteria better
than agents. In practice, agents with criteria *they proposed* execute with more buy-in —
and proposed criteria are more likely to be browser-verifiable because the Generator writes
them with testability in mind.

### Pattern: Generator proposes → Evaluator reviews → confirm

```python
# In agents/generator.py — propose_contract()
_PROPOSE_TOOL = {
    "name": "propose_criteria",
    "input_schema": {
        "type": "object",
        "properties": {
            "success_criteria": {
                "type": "array", "items": {"type": "string"},
                "description": "3-6 browser-verifiable criteria for this sprint",
            },
            "evidence": {
                "type": "object",
                "description": "Routes, commands, API probes, source files, and artifacts the Evaluator should collect.",
            },
            "rationale": {"type": "string"},
        },
        "required": ["success_criteria", "evidence", "rationale"],
    },
}

def propose_contract(spec, sprint_goal, out_of_scope, sprint_number, handoff=None):
    # Generator proposes criteria based on SPEC + goal
    # Returns SprintContract with confirmed=False
    ...

def revise_contract(spec, contract, issues, handoff=None):
    # Generator addresses Evaluator's objections, re-proposes
    ...
```

```python
# In agents/evaluator.py — review_contract()
_REVIEW_TOOL = {
    "name": "review_criteria",
    "input_schema": {
        "type": "object",
        "properties": {
            "approved": {"type": "boolean"},
            "issues": {
                "type": "array", "items": {"type": "string"},
                "description": "One entry per criterion that fails review: 'SC-N: reason'",
            },
        },
        "required": ["approved", "issues"],
    },
}

def review_contract(spec, contract):
    # Evaluator checks: browser-verifiable? unambiguous? within scope?
    # Returns (approved: bool, issues: list[str])
    ...
```

```python
# In harness.py — negotiate_contract()
def negotiate_contract(spec, sprint_number, handoff=None):
    goal, out_of_scope = _load_sprint_seed(sprint_number)  # from harness-state/sprints.md
    contract = propose_contract(spec, goal, out_of_scope, sprint_number, handoff)
    for _ in range(2):  # max 2 review rounds
        approved, issues = review_contract(spec, contract)
        if approved:
            break
        contract = revise_contract(spec, contract, issues, handoff)
    contract.confirmed = True
    return contract
```

`harness-state/sprints.md` should contain only `goal` and `out_of_scope` seeds — NOT
criteria. The agents generate and validate criteria dynamically, then the harness writes
the confirmed result to `harness-state/contracts/contract-sprint-N.json`.

### Interactive (use when human wants direct control)

The `negotiate_contract()` function in `harness.py` collects criteria via `input()`.
User types each success criterion one at a time, confirms, and the harness proceeds.

Best for: when the user is present and wants to guide each sprint.

### Config-File (for full automation — criteria pre-written by human)

Replace `negotiate_contract()` with a loader that reads confirmed contract JSON from
`harness-state/contracts/`:

```python
import json

def load_contract(sprint_number: int, contracts_dir: Path) -> SprintContract:
    """Load sprint contract from a JSON config file."""
    sprint = json.loads((contracts_dir / f"contract-sprint-{sprint_number}.json").read_text())
    criteria = [
        SuccessCriterion(**sc)
        for sc in sprint["success_criteria"]
    ]
    return SprintContract(
        sprint_number=sprint_number,
        goal=sprint["goal"],
        success_criteria=criteria,
        out_of_scope=sprint.get("out_of_scope", []),
        evidence=sprint.get("evidence", {}),
        confirmed=True,
    )
```

## Evidence Field

Add this optional field to `SprintContract`:

```python
evidence: dict = field(default_factory=dict)
```

Recommended JSON shape:

```json
{
  "evidence": {
    "routes": ["/", "/account/profile"],
    "api": [
      {"method": "GET", "path": "/api/auth/session", "expectStatus": 200}
    ],
    "commands": [
      {"name": "build", "cmd": ["npm", "run", "build"]}
    ],
    "source_files": ["src/app/api/health/ready/route.ts"],
    "negative_tests": ["Missing required env should make readiness fail"],
    "public_routes": []
  }
}
```

Rules:

- If a criterion needs a command, declare it under `commands`.
- If a criterion needs source review, declare specific files under `source_files`.
- If a criterion needs an endpoint, declare it under `api`.
- Keep `public_routes` empty unless there is no safer evidence path.
- All evidence output goes under `harness-state/evidence/sprint-N/`.

Sprint seed format (`harness-state/sprints.md`):
```markdown
# Sprints

## Sprint 1 — Create and view todo items
Goal: User can create and view todo items.
Out of scope:
- editing items
- deleting items
- authentication
```

Best for: CI/CD pipelines, fully automated harness runs, scheduled builds.

---

## Contract Anti-Patterns Reference

| Anti-Pattern | Example | Fix |
|---|---|---|
| Code reference | "The sendEmail function exists" | "Submitting the form sends an email to the address entered" |
| Vague | "The app is fast" | "The list renders within 1 second of page load" |
| Circular | "Login works" | "Entering valid credentials and clicking Login shows the dashboard" |
| Over-scoped | All MVP features in Sprint 1 | Split into focused sprints with ≤ 5 criteria each |
| Missing out-of-scope | _(empty list)_ | Always list what NOT to build; prevents generator over-building |
| Undeclared evidence | "Build passes" with no command | Add `evidence.commands: [{"name":"build","cmd":["npm","run","build"]}]` |
| Public test artifact | `/api/sprint-12/evidence` | Prefer harness evidence JSON; if public route is unavoidable, declare cleanup |
