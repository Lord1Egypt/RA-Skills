## Description:

Use when managing Feishu/Lark Drive files through lark-cli or feishu-cli for Dev Hub search, inspect, upload, download, import, export, sync, comments, permissions, and artifact registration.

This skill is ready for commercial/non-commercial use.

## Publisher:

[afengzi](https://clawhub.ai/user/afengzi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and teams use this skill to manage Feishu/Lark Drive files in Dev Hub workflows, including discovery, inspection, import, export, sync, comments, permissions, and artifact registration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Drive sync, upload, export, permission, and artifact writeback actions can affect files or workspace records in the authenticated Lark/Feishu account.

Mitigation: Review proposed commands before execution and confirm lark-cli is authenticated to the intended account and workspace.

Risk: Downloaded private files may be retained locally if a workflow stores them in the repository.

Mitigation: Follow the skill guidance to avoid storing downloaded private files in the repo unless the user explicitly requests it.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/afengzi/skills/lark-cli-devhub-drive)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires an authenticated lark-cli or feishu-cli session for Drive operations.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
