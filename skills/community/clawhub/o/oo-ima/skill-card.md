## Description:

ima (ima.qq.com). Use this skill for ANY ima request — reading, creating, and updating data. Whenever a task involves ima, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and assistants use this skill to search and read IMA notes and knowledge bases, and to create or update IMA content through an OOMOL-connected account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup fallback runs a remote installer without a separate approval step, and the installer was not verified.

Mitigation: Install a verified, pinned oo CLI release yourself before using the skill.

Risk: The connected IMA account can be used for actions that create or change content.

Mitigation: Review the connected account's permissions and confirm the exact effect of each write before running it.

## Reference(s):

- [oo CLI](https://github.com/oomol-lab/oo-cli)
- [IMA homepage](https://ima.qq.com)
- [IMA agent interface documentation](https://ima.qq.com/agent-interface)
- [ClawHub release page](https://clawhub.ai/oomol/skills/oo-ima)

## Skill Output:

**Output Type(s):** [Text, JSON, Markdown, Guidance]

**Output Format:** [Natural-language responses with retrieved text or structured IMA results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Available results depend on the connected IMA account and selected action.]

## Skill Version(s):

1.0.7 (source: skill frontmatter and server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
