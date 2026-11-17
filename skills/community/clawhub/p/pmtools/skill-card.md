## Description:

Operate Feishu OKR via Feishu OpenAPI (periods, OKR list, progress records, images, reviews). Invoke when you need to query or update OKR progress.

This skill is ready for commercial/non-commercial use.

## Publisher:

[taoxiang-org](https://clawhub.ai/user/taoxiang-org)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use pmtools to query and update Feishu OKR periods, OKRs, progress records, images, and reviews from an agent-assisted workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can modify Feishu OKR data, including progress records and period status.

Mitigation: Review proposed commands before execution, confirm destructive or status-changing operations, and use least-privilege Feishu credentials.

Risk: Automatic self-update can change local skill code before commands run.

Mitigation: Disable auto-update with PM_TOOLS_DISABLE_AUTO_UPDATE=1, pin reviewed versions, and update only from trusted sources.

Risk: Tenant access tokens may be cached locally.

Mitigation: Use restricted credentials, protect the token cache path, avoid plaintext token persistence where policy prohibits it, and clear cached tokens after use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/taoxiang-org/skills/pmtools)
- [Feishu OpenAPI](https://open.feishu.cn/open-apis)
- [Feishu OKR OpenAPI v1](https://open.feishu.cn/open-apis/okr/v1)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands require Feishu credentials and may read or modify OKR records depending on the selected command.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
