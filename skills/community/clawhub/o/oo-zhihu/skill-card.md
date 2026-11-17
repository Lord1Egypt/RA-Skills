## Description:

Zhihu (zhihu.com). Use this skill for ANY Zhihu request — reading, creating, and updating data. Whenever a task involves Zhihu, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

People using an OOMOL-connected Zhihu account can search and read Zhihu content, inspect account collections and followees, query Zhida knowledge bases, and request PDF parsing or presentation generation. The skill also supports writes such as knowledge-base uploads and Zhida chats, which require user confirmation under its instructions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup fallback can execute downloaded CLI installation code without a separate approval step; the downloaded installer and hosted implementation were not verified in the supplied review.

Mitigation: Use setup only after a matching authentication or connection failure. Review the installer and its installation and synchronization behavior, then approve the installation separately.

Risk: Using the skill involves OOMOL-mediated account access, and selected actions upload content to Zhihu or change Zhida state.

Mitigation: Understand which account data and files the selected action sends to Zhihu, and preserve the skill's requirement to confirm the exact payload and effect before write actions.

## Reference(s):

- [Zhihu](https://www.zhihu.com)
- [oo CLI repository (linked by the skill)](https://github.com/oomol-lab/oo-cli)
- [oo CLI installation guide](https://cli.oomol.com/install-guide.md)
- [Zhihu skill release on ClawHub](https://clawhub.ai/oomol/skills/oo-zhihu)

## Skill Output:

**Output Type(s):** [API Calls, Text, JSON]

**Output Format:** [JSON connector responses with textual results or guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results depend on the selected action and the connected Zhihu account.]

## Skill Version(s):

1.0.6 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
