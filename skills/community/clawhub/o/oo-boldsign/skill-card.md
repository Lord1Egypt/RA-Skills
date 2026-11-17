## Description:

BoldSign (boldsign.com). Use this skill for ANY BoldSign request — reading, creating, and updating data. Whenever a task involves BoldSign, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Users with an OOMOL-connected BoldSign account can inspect documents and templates, list records, check API credits, and send signature requests from existing templates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup runs remote CLI installers without clear approval, and automatic synchronization could change other agent skills.

Mitigation: Review and approve CLI installation separately; prefer a pinned, verified release; and review or disable automatic skill synchronization across agents.

## Reference(s):

- [BoldSign](https://boldsign.com)
- [BoldSign API documentation](https://developers.boldsign.com/)
- [oo CLI repository](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Guidance]

**Output Format:** [CLI commands and JSON responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Action inputs are checked against live schemas; one action sends a signature request from an existing template.]

## Skill Version(s):

1.0.4 (source: frontmatter, server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
