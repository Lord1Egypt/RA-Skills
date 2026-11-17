## Description:

Use when a DevOps or SRE team needs to write a blameless postmortem after a production incident. Guides timeline reconstruction, root cause analysis, and produces a complete postmortem document with prioritized action items.

This skill is ready for commercial/non-commercial use.

## Publisher:

[archlab-space](https://clawhub.ai/user/archlab-space)

### License/Terms of Use:

MIT-0

## Use Case:

DevOps, SRE, and incident response teams use this skill to facilitate a structured, blameless retrospective after a resolved production incident and draft a shareable postmortem with timeline, impact, root cause, and action items.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Incident timelines and draft postmortems may contain credentials, customer PII, tokens, raw sensitive logs, or other confidential operational data.

Mitigation: Redact sensitive data before providing incident details and remove any sensitive material from the generated draft before circulation.

Risk: Security, P0, regulatory, or legal-impact incidents may require review beyond the generated postmortem draft.

Mitigation: Review the final document with the appropriate security, legal, compliance, or internal incident team before sharing.

Risk: A generated root-cause analysis or action plan can be incomplete if the timeline, RCA focus areas, owners, or due dates are missing.

Mitigation: Treat the output as a draft and confirm the timeline, root cause, measurable action items, owners, and due dates with the incident team.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/archlab-space/skills/incident-postmortem)

## Skill Output:

**Output Type(s):** [guidance, markdown, text]

**Output Format:** [Conversational guidance and Markdown postmortem document]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces a draft for human review; does not publish, send, or share the postmortem on behalf of the user.]

## Skill Version(s):

0.1.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
