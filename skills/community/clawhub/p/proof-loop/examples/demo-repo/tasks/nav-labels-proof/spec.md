# Task: nav-labels-proof

## Task Statement

Make sure the demo navigation labels contain the expected English and German strings.

## Acceptance Criteria

**AC1:** English navigation labels contain Home, Settings, and Billing.
- Verify: `python3 examples/demo-repo/check_nav_labels.py examples/demo-repo/nav_labels.json`

**AC2:** German navigation labels contain Startseite, Einstellungen, and Abrechnung.
- Verify: `python3 examples/demo-repo/check_nav_labels.py examples/demo-repo/nav_labels.json`

**AC3:** The check command exits non-zero if the labels drift.
- Verify: inspect `examples/demo-repo/check_nav_labels.py`; it compares the JSON file against the expected dictionary and returns `1` on mismatch.

## Constraints

- Keep the fixture tiny and dependency-free.
- Keep labels in a human-readable JSON file.

## Non-Goals

- Building a real web app.
- Adding translation infrastructure.

## Verification Approach

Run the demo check command and then run `scripts/check_task.py examples/demo-repo/tasks/nav-labels-proof`.
