## Description: <br>
Audit a NousResearch/hermes-agent checkout or fork for Hermes-specific runtime-contract drift, command-surface splits, memory/skill/gateway health, and agent architecture risks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[huangrichao2020](https://clawhub.ai/user/huangrichao2020) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and maintainers use this skill to audit Hermes Agent checkouts, forks, and deployment support repositories for runtime-contract drift, command-surface consistency, memory and skill architecture, gateway readiness, observability, and prioritized fix planning. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill relies on installing and running the third-party hermescheck Python package against local source code. <br>
Mitigation: Run it in a virtual environment or container, and pin or inspect the package before use in sensitive repositories. <br>
Risk: Generated JSON, Markdown, or SARIF reports may contain local paths or secret-detection evidence from the audited repository. <br>
Mitigation: Review generated reports before sharing them outside the intended review group. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/huangrichao2020/hermes-agent-health-check) <br>
- [Code-Level Anti-Patterns](references/code-patterns.md) <br>
- [Playbooks](references/playbooks.md) <br>
- [Audit Report Schema](references/report-schema.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and references to structured JSON, Markdown, and SARIF audit reports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The underlying hermescheck reports can include local paths and secret-detection evidence; review generated reports before sharing them.] <br>

## Skill Version(s): <br>
1.1.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
