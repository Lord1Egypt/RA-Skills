# Portfolio Dashboard · {{ project.name }}

> Monitors each component's health and schedule performance (CPI/SPI) from a portfolio perspective, supporting prioritization and resource scheduling.

## Component Health Dashboard
| Component | Methodology | Health | CPI | SPI | Owner | Notes |
|------|--------|--------|-----|-----|--------|------|
{{#each components}}
| {{this.name}} | {{this.methodology}} | {{ sev_icon(this.health) }} {{this.health}} | {{this.cpi}} | {{this.spi}} | {{this.owner}} | {{this.note}} |
{{/each}}

## Interpretation
- **Health**: 🟢 Green (normal) / 🟡 Yellow (watch) / 🔴 Red (alert).
- **CPI** (Cost Performance Index): >1 under budget, =1 on budget, <1 over budget.
- **SPI** (Schedule Performance Index): >1 ahead, =1 on track, <1 behind.

> Tip: Components with Red health or CPI/SPI < 0.9 should enter the governance meeting for focused tracking.
