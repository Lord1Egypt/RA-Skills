Expected output:

- Starts in `WAITING_FOR_LOGIC_CONFIRMATION`, because the sample provides enough context but has not approved the proposed workflow.
- Produces an intake summary, decision-dependency check, task card, Loop-fit judgment, recommended artifact, and work-logic confirmation card.
- Selects `Plan-Execute-Verify` as the primary mode and may use bounded retry as a supporting strategy.
- Derives a small maximum iteration count from feedback cost, reversibility, and risk instead of using an unexplained default.
- Defines explicit stop conditions for no improvement, scope drift, test weakening, permission risk, and missing evidence.
- Does not inspect the project, run commands, edit files, or generate the final executable Loop before the user confirms the logic.
