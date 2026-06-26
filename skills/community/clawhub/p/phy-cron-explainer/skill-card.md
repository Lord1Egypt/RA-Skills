## Description: <br>
Explains, validates, converts, and audits cron expressions across major flavors, showing plain English meanings and next run times. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[PHY041](https://clawhub.ai/user/PHY041) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to understand cron schedules, validate expressions before deployment, convert plain-English schedules to cron, and audit cron entries in workflow, Kubernetes, and crontab files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Next-run calculations may trigger an automatic pip install of croniter if the dependency is unavailable. <br>
Mitigation: Review before installing, preinstall a reviewed croniter dependency, or remove the fallback package-install behavior. <br>
Risk: Scan mode reads workflow, Kubernetes, and crontab files from the directories selected by the user. <br>
Mitigation: Run scan mode only against directories whose scheduling files the agent is intended to inspect. <br>


## Reference(s): <br>
- [Phy Cron Explainer on ClawHub](https://clawhub.ai/PHY041/phy-cron-explainer) <br>
- [Canlah AI](https://canlah.ai) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Guidance] <br>
**Output Format:** [Markdown with cron expressions, tables, diagnostics, and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include next-run timestamps, validation issues, suggested fixes, scan summaries, and converted cron expressions.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata and skill metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
