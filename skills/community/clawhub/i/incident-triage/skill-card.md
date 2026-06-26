## Description: <br>
Structured incident triage for alerts from any monitoring source, using a five-step framework to classify severity, scope blast radius, correlate recent changes, investigate by alert type, and act. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ggettert](https://clawhub.ai/user/ggettert) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and site reliability engineers use this skill to triage operational alerts, correlate incidents with recent GitHub activity, summarize findings, create incident tickets, and decide whether to escalate. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: GitHub CLI usage may rely on credentials with access to repositories, CI history, and issue creation. <br>
Mitigation: Use least-privilege GitHub CLI credentials scoped to the repositories and actions needed for incident triage. <br>
Risk: The runbook template contains placeholders and may be unreliable until customized for the user's infrastructure. <br>
Mitigation: Fill in services, endpoints, dashboards, log locations, deployment paths, and on-call contacts before relying on the skill during an incident. <br>
Risk: Incident issue creation can notify teams or publish sensitive incident details to a repository. <br>
Mitigation: Require human confirmation before creating incident issues unless automatic ticket creation is explicitly desired. <br>


## Reference(s): <br>
- [Triage Framework](references/triage-framework.md) <br>
- [Alert Patterns](references/alert-patterns.md) <br>
- [Escalation Guide](references/escalation-guide.md) <br>
- [Runbook Template](references/runbook-template.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with incident summaries, checklists, and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May use GitHub CLI helper scripts when available; requires user-provided alert details and appropriate credentials.] <br>

## Skill Version(s): <br>
0.3.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
