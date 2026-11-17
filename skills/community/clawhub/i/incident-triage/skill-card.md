## Description:

Structured incident triage for alerts from common monitoring sources, using a five-step workflow to classify severity, scope impact, correlate recent changes, investigate by alert type, and decide the next action.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ggettert](https://clawhub.ai/user/ggettert)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, SREs, and on-call engineers use this skill to turn raw alerts or incident descriptions into structured triage, investigation, escalation, and ticket-creation steps.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The bundled runbook is a template and may contain placeholder services, dashboards, endpoints, and contacts.

Mitigation: Populate the runbook with approved infrastructure details before relying on the skill during a real incident.

Risk: The GitHub issue creation helper can publish an incident issue body to the target repository.

Mitigation: Review the issue body, severity, title, repository, and labels before running the issue creation script.

Risk: Deeper investigation for monitoring tools may require access to external dashboards or APIs.

Mitigation: Use organization-approved credentials and verify alert details in the source monitoring system before taking operational action.

## Reference(s):

- [Triage Framework](references/triage-framework.md)
- [Alert Patterns](references/alert-patterns.md)
- [Escalation Guide](references/escalation-guide.md)
- [Runbook Template](references/runbook-template.md)
- [ClawHub Skill Page](https://clawhub.ai/ggettert/skills/incident-triage)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with checklists, incident summaries, escalation text, and inline bash commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May use GitHub CLI helper scripts for deploy correlation, merge correlation, and incident issue creation when the user supplies repository context.]

## Skill Version(s):

0.3.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
