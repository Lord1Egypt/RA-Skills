## Description:

Production-ready incident response runbook templates with step-by-step procedures for detection, triage, mitigation, resolution, communication, escalation, on-call onboarding, and post-incident review.

This skill is ready for commercial/non-commercial use.

## Publisher:

[solomonneas](https://clawhub.ai/user/solomonneas)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, site reliability engineers, incident commanders, and on-call teams use this skill to draft service-specific incident runbooks, escalation paths, recovery procedures, communication templates, and post-incident review formats.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Runbook examples include high-impact production commands such as rollbacks, scaling changes, feature flag updates, network policy changes, backend termination, and database maintenance.

Mitigation: Treat generated runbooks as drafts and add explicit approval gates, environment and tenant scoping, owner signoff, safer alternatives, and post-action validation before operational use.

Risk: Incident response templates can be copied into production workflows without enough local context for the affected service, dependencies, data sensitivity, or blast radius.

Mitigation: Require responders to tailor each template with service owners, escalation paths, read-only preview steps, backup checks, rollback conditions, and verification steps before use.

## Reference(s):

- [Google SRE Book - Incident Management](https://sre.google/sre-book/managing-incidents/)
- [PagerDuty Incident Response](https://response.pagerduty.com/)
- [Atlassian Incident Management](https://www.atlassian.com/incident-management)
- [ClawHub skill page](https://clawhub.ai/solomonneas/skills/incident-runbook-templates)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell, SQL, YAML, and checklist examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include production incident response commands and templates that require human review before operational use.]

## Skill Version(s):

1.0.1 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
