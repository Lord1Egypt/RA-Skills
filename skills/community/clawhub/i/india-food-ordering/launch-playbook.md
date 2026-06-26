# Launch playbook

## Phase 1: Connector readiness

- Verify Swiggy and Zomato connector status.
- Document capability matrix from `setup.md`.

## Phase 2: Safety simulation

- Run mock ordering scenarios:
  - happy path
  - missing address
  - unavailable item
  - primary vendor failure + fallback

## Phase 3: Human QA

- Validate confirmation copy and risk warnings.
- Ensure no order is placed prior to explicit confirmation.

## Phase 4: Controlled rollout

- Start with one city/location scope.
- Monitor failure modes and duplicate-order risk.
- Expand only after validation checklist passes.

