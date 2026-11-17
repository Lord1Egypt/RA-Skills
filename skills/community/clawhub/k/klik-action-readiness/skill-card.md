## Description:

Creates a compact Action Readiness Card for reviewing source, freshness, scope, authority, expected result, and human-return conditions before an AI prepares a consequential next step from remembered Context.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chengyixu](https://clawhub.ai/user/chengyixu)

### License/Terms of Use:

MIT-0

## Use Case:

People, agents, and workflow designers use this skill to decide whether an AI should prepare a bounded next step from remembered Context. It helps make missing source, freshness, scope, authority, expected result, and human-return conditions explicit before any preparation occurs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may mistake the Action Readiness Card for approval to execute a real-world action.

Mitigation: Use the card only as a planning and review aid; return to a person before new access, material judgment, external commitments, or tool actions.

Risk: Sensitive context could be over-collected while evaluating readiness.

Mitigation: Use short, redacted context summaries and avoid credentials, recordings, transcripts, client data, financial data, health data, and other sensitive material.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chengyixu/skills/klik-action-readiness)
- [Klik pre-launch direction](https://pre.hiklik.ai/?utm_source=clawhub&utm_medium=companion_skill&utm_campaign=kickstarter_prelaunch&utm_content=action_readiness)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown Action Readiness Card]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses short, redacted context summaries; does not authorize or execute actions.]

## Skill Version(s):

1.0.1 (source: server release metadata, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
