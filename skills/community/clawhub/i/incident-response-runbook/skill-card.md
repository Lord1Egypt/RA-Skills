## Description:

Create, maintain, and execute detailed incident response runbooks to guide triage, communication, and post-incident reviews for production outages.

This skill is ready for commercial/non-commercial use.

## Publisher:

[charlie-morrison](https://clawhub.ai/user/charlie-morrison)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, site reliability engineers, and on-call responders use this skill to create incident runbooks, triage outages, draft stakeholder communications, and prepare post-incident reviews for production systems.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated diagnostic, rollback, or communication steps may be inaccurate or unsuitable for a live production incident.

Mitigation: Review and adapt generated steps before production use, especially commands that affect deployments, traffic, data stores, or public communications.

Risk: Incident descriptions, timelines, logs, or runbook prompts may contain secrets or sensitive operational details.

Mitigation: Use only approved environments for sensitive incident data and remove secrets before providing prompts or generated materials to an agent.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/charlie-morrison/skills/incident-response-runbook)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown runbooks with checklists, command examples, communication templates, and post-incident review sections]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The bundled script can write a generated Markdown runbook to a user-specified output path.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
