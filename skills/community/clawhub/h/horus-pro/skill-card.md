## Description:

Horus Pro generates meeting summaries, decisions, action trackers, stakeholder-specific briefs, next meeting agendas, risk flags, and follow-up emails from meeting notes or transcripts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[occupythemilkyway](https://clawhub.ai/user/occupythemilkyway)

### License/Terms of Use:

MIT-0

## Use Case:

External users and workplace teams use this skill to turn raw meeting notes or transcripts into a meeting brief, action tracker, follow-up email, next agenda, and stakeholder-specific briefs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The install step changes the host Python environment by installing an unpinned package.

Mitigation: Install in a virtual environment and pin the dependency version before use.

Risk: Generated files may contain sensitive meeting, personnel, customer, or business information.

Mitigation: Use a private OUTPUT_DIR and review access controls before sharing or syncing outputs.

## Reference(s):

- [Horus Pro ClawHub Skill Page](https://clawhub.ai/occupythemilkyway/skills/horus-pro)
- [Horus Pro Homepage](https://clawhub.ai/occupythemilkyway/horus-pro)

## Skill Output:

**Output Type(s):** [Text, Markdown, Files, Shell commands, Configuration]

**Output Format:** [Markdown files with setup shell commands and environment-variable configuration]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces five Markdown documents in OUTPUT_DIR; generated files may contain sensitive meeting, personnel, customer, or business information.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
