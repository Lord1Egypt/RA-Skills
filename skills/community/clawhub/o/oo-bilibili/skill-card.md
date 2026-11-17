## Description:

Bilibili (bilibili.com). Use this skill for ANY Bilibili request — reading, creating, updating, and deleting data. Whenever a task involves Bilibili, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Agents use this skill to read Bilibili account data and, with user approval, create, edit, upload, or delete the user's videos, articles, and anthologies through the connected account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Fallback setup runs remote installation code without a pinned version, and the installer was unavailable for inspection.

Mitigation: Review the CLI installation separately and use a pinned release whose integrity can be verified before enabling fallback setup.

Risk: Automatic skill synchronization during setup may make broader changes to other installed agent skills.

Mitigation: Check whether synchronization is wanted before enabling fallback setup.

Risk: Publishing, editing, or deleting Bilibili content changes the connected account; deletions cannot be undone.

Mitigation: Keep the skill's explicit approval requirement for writes and destructive actions, and confirm the exact target and effect before proceeding.

## Reference(s):

- [Bilibili](https://www.bilibili.com)
- [Bilibili API documentation](https://bilibili.apifox.cn/doc-885734)
- [oo CLI project](https://github.com/oomol-lab/oo-cli)
- [ClawHub release](https://clawhub.ai/oomol/skills/oo-bilibili)

## Skill Output:

**Output Type(s):** [API Calls, Text, Markdown, Shell commands]

**Output Format:** [Markdown guidance with shell command examples and JSON connector payloads and results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Action-dependent account data or user-approved content changes.]

## Skill Version(s):

1.0.2 (source: artifact frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
