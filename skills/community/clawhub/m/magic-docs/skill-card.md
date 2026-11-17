## Description:

Magic Docs helps an agent keep marked Markdown documents current by detecting relevant new information after each conversation and updating those files.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wavmson](https://clawhub.ai/user/wavmson)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to create or maintain living project documentation by marking Markdown files with a Magic Doc comment and updating them when conversations contain durable new facts, decisions, or corrections.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automatic workspace scanning and Markdown updates can persist sensitive workspace or operational details.

Mitigation: Use this skill only where automatic Markdown edits are acceptable, mark specific non-sensitive documents, and avoid using it for passwords, credentials, internal network inventories, device access details, MEMORY.md, TOOLS.md, or other private state.

Risk: Realtime updates can add information before a user has reviewed whether it belongs in long-lived documentation.

Mitigation: Prefer scoped Magic Doc markers and daily or manual update modes for higher-risk documents, then review document diffs before relying on the updated content.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/wavmson/skills/magic-docs)

## Skill Output:

**Output Type(s):** [markdown, shell commands, guidance]

**Output Format:** [Markdown files and concise Markdown update notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Updates are scoped by MAGIC DOC markers, optional scope keywords, and update frequency settings.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
