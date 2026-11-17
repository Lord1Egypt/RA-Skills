## Description:

Nova 自驱动轨道 — GitHub调研 + 自进化记忆 + 模式复用 + 人机协作。Nova 的核心智能引擎。

This skill is ready for commercial/non-commercial use.

## Publisher:

[jokerli530](https://clawhub.ai/user/jokerli530)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external agent users use this skill to guide a Nova agent through recurring GitHub research, pattern reuse, persistent memory updates, self-assessment, and local status reporting workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow can write persistent local memory and update pattern or skill files.

Mitigation: Require review before memory, pattern, or skill updates and use it only in workspaces where persistent agent notes are acceptable.

Risk: The workflow may run a local self-assessment script and post status to localhost services.

Mitigation: Review or disable the external script path and local service integration before installation.

Risk: The workflow can send task context through ByteRover and GitHub requests via a local proxy.

Mitigation: Avoid using the skill with secrets, credentials, or proprietary task text unless those integrations are approved.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jokerli530/skills/nova-orbit)
- [Publisher profile](https://clawhub.ai/user/jokerli530)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown with inline bash code blocks and workflow checklists]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May direct the agent to write persistent local memory, update pattern files, call local services, use ByteRover, query GitHub through a local proxy, and run a local self-assessment script.]

## Skill Version(s):

1.0.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
