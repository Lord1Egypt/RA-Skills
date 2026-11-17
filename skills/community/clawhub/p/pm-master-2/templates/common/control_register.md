# Control Register

> The mandatory **recurring control checklist** that must be established at the start of the operational period: defines "what to inspect / frequency / owner / trigger conditions / last result".
> This is the disciplinary foundation for the PM Control Engine; consistency gates will alert when items are missing.

| Item | Content |
|----|------|
| Project Name | {{ project.name }} ({{ project.id }}) |
| Control Owner | {{ project.pm }} |
| Inspection Frequency (cadence) | {{#if control}}{{ control.cadence }}{{#else}} (Not configured: set control.cadence in project.yaml) {{/if}} |
| Escalation Threshold | {{#if control}}{{#if control.thresholds}}SPI<{{control.thresholds.spi_warn}} / CPI<{{control.thresholds.cpi_warn}} / Schedule slip≥{{control.thresholds.schedule_slip_pct}}% / Open changes≥{{control.thresholds.open_change_high}}{{#else}} (Default) {{/if}}{{#else}} (Default) {{/if}} |

## Recurring Controls

| # | Control Item | Baseline Comparison Calculation | Default Escalation Threshold | Frequency | Last Result |
|---|--------|--------------|--------------|------|------------|
| 1 | Schedule | Per-WBS-package planned% vs actual% variance / overdue days | Slip≥15% or overdue incomplete | {{#if control}}{{control.cadence}}{{#else}}—{{/if}} | Awaiting first inspection |
| 2 | Cost EVM | SPI=EV/PV, CPI=EV/AC, EAC/ETC/VAC | SPI<0.95 or CPI<0.95 | {{#if control}}{{control.cadence}}{{#else}}—{{/if}} | Awaiting first inspection |
| 3 | Risk Drift | Current score vs baseline score; new red/severe risks | Score escalation or new high/severe risk | Per review cycle | Awaiting first inspection |
| 4 | Milestone | Milestone date passed and incomplete | Overdue incomplete | Before each milestone | Awaiting first inspection |
| 5 | Issue RAID | Issue due passed and not closed | Overdue not closed | Weekly | Awaiting first inspection |
| 6 | Change | Number of open change requests | Open count≥2 | Per CCB | Awaiting first inspection |
| 7 | Data Integrity | Re-run consistency_check | Gate failure | Each inspection | Awaiting first inspection |

## Operation Mode

```
python3 control_engine.py --project <project.yaml> [--as-of YYYY-MM-DD]
```

- Outputs `control_report.md` + structured JSON; when overall status is **RED, exit code 1**, can be hooked to scheduled tasks / automated periodic inspection and alerting.
- Recipients: {{#if control}}{{#if control.recipients}}{{#each control.recipients}}{{this}} {{/each}}{{#else}} (Not configured) {{/if}}{{#else}} (Not configured) {{/if}}
