## Description:

同步主Agent的配置文件和目录至动态Agent工作区，确保动态Agent与主Agent配置一致且自动覆盖更新。

This skill is ready for commercial/non-commercial use.

## Publisher:

[jobzhao15](https://clawhub.ai/user/jobzhao15)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to sync main-agent instructions, memory, tools, skills, and related configuration into dynamic-agent workspaces for channels such as WeCom or WhatsApp.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can persistently overwrite dynamic-agent instruction, memory, tool, skill, and configuration files.

Mitigation: Install only when the publisher is trusted and this synchronization behavior is needed; review target workspaces and keep a recovery path for overwritten files.

Risk: Unchecked agent IDs can redirect writes outside the intended dynamic-agent workspace.

Mitigation: Validate agent IDs, enforce destination containment under the intended .openclaw workspace, and avoid passing untrusted input as agentId.

Risk: Synchronization occurs without a dry-run or confirmation path.

Mitigation: Prefer adding dry-run or confirmation behavior before use in workflows where dynamic-agent state must be preserved.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jobzhao15/skills/huo15-agent-extension)

## Skill Output:

**Output Type(s):** [Files, Configuration, Text]

**Output Format:** [Filesystem copies with string status details]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Copies selected configuration files and recursively syncs skills/ and memory/ into dynamic-agent workspaces, overwriting conflicts with main-agent content.]

## Skill Version(s):

1.0.0 (source: evidence.json release.version and artifact/package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
