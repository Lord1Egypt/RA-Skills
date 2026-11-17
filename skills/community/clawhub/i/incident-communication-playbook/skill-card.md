## Description:

Write professional incident updates, blameless postmortems, maintenance announcements, and status reports for a status page.

This skill is ready for commercial/non-commercial use.

## Publisher:

[openstatus](https://clawhub.ai/user/openstatus)

### License/Terms of Use:

MIT-0

## Use Case:

On-call engineers, SREs, DevOps teams, and engineering managers use this skill pack to configure status-page context and draft incident updates, postmortems, maintenance announcements, and periodic status reports for users or stakeholders.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Drafted incident or status communications may contain incorrect, incomplete, or premature operational details if source incident data is incomplete.

Mitigation: Review drafts before posting them publicly, especially incident details, timestamps, customer impact, and approval requirements.

Risk: The setup skill can read limited project files and write .agents/status-page-context.md for future status communications.

Mitigation: Confirm the generated context contains appropriate service, component, SLA, tone, and escalation information before relying on it for public communications.

## Reference(s):

- [OpenStatus homepage](https://openstatus.dev)
- [ClawHub skill page](https://clawhub.ai/openstatus/skills/incident-communication-playbook)
- [Package overview](artifact/skills.md)
- [README](artifact/README.md)
- [Incident communication framework](artifact/skills/incident-communication/references/framework.md)
- [Postmortem framework](artifact/skills/postmortem/references/framework.md)
- [Maintenance framework](artifact/skills/maintenance/references/framework.md)
- [Status report framework](artifact/skills/status-report/references/framework.md)
- [Status page context framework](artifact/skills/status-page-context/references/framework.md)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown drafts and structured guidance for status-page communications]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update .agents/status-page-context.md for shared status-page context; communication drafts should be reviewed before publication.]

## Skill Version(s):

1.0.0 (source: server release metadata and package frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
