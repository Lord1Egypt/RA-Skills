## Description:

Two-stage intelligent filtering and scoring of CRM contacts using keywords and AI, adapting over time to prioritize leads that matter most to the user.

This skill is ready for commercial/non-commercial use.

## Publisher:

[odinbot33](https://clawhub.ai/user/odinbot33)

### License/Terms of Use:


## Use Case:

Agents and CRM users use this skill to filter contact lists, score individual leads, prioritize follow-up, and preserve filtering preferences across runs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Contact metadata may be sent to Anthropic during Stage 2 scoring when ANTHROPIC_API_KEY is configured.

Mitigation: Use the skill only with contacts approved for external processing, run without ANTHROPIC_API_KEY for local Stage 1 filtering, or add explicit opt-in and field minimization before AI scoring.

Risk: Rejected contacts can be persisted in learning.json without strong review or clearing controls.

Mitigation: Review learning.json regularly, provide a process to clear rejected_contacts, and avoid storing confidential or regulated contact data there.

Risk: The release evidence does not provide a license identifier.

Mitigation: Confirm the license with the publisher before commercial reuse or redistribution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/odinbot33/skills/oee-crm-intelligence)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash examples; JSON objects, sorted result lists, or text summaries on stdout when the tool is run]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Stage 2 scoring can call Anthropic when ANTHROPIC_API_KEY is configured; rejected contacts can be persisted in learning.json.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
