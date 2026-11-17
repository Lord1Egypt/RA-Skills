## Description:

Alibaba Cloud STS (alibabacloud.com). Use this skill for ANY Alibaba Cloud STS request — reading, creating, and updating data. Whenever a task involves Alibaba Cloud STS, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers can use this skill to inspect Alibaba Cloud STS action schemas and run AssumeRole or federated-credential requests through a connected OOMOL account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automatic setup may make lasting changes to the agent environment that the skill does not explain.

Mitigation: Review setup steps before enabling the skill, install a vetted CLI release, and consider disabling startup skill synchronization with OO_SKILLS_SYNC_DISABLED=1.

Risk: AssumeRole and federation actions can return temporary cloud credentials, and the downloaded installers and hosted connector behavior were not verified.

Mitigation: Use narrowly scoped cloud permissions, protect returned credentials, and review the setup and CLI release before use.

## Reference(s):

- [oo CLI](https://github.com/oomol-lab/oo-cli)
- [Alibaba Cloud RAM product page](https://www.alibabacloud.com/product/ram)
- [Alibaba Cloud STS API documentation](https://www.alibabacloud.com/help/en/ram/developer-reference/api-sts-2015-04-01-overview)
- [oo CLI installation guide](https://cli.oomol.com/install-guide.md)
- [OOMOL Alibaba Cloud STS connection setup](https://console.oomol.com/connections/aliyun_sts)

## Skill Output:

**Output Type(s):** [API Calls, Shell commands, Guidance]

**Output Format:** [JSON API responses with Markdown command and setup guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Responses may include temporary Alibaba Cloud STS credentials; use narrowly scoped permissions and protect credentials.]

## Skill Version(s):

1.0.7 (source: release evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
