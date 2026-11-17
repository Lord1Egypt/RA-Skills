## Description:

在 NAS、Linux、Windows 或 macOS 上部署并自检本地 SearXNG 搜索服务。

This skill is ready for commercial/non-commercial use.

## Publisher:

[linkkhub-pixiu](https://clawhub.ai/user/linkkhub-pixiu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and Agent users can use this skill to deploy and check a local SearXNG search service, then connect it to OpenClaw or another supported Agent.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search requests may reach external search engines, despite the local-service privacy claim.

Mitigation: Assume queries can leave the network and avoid confidential or identifying search terms.

Risk: Missing deployment files leave container permissions and network exposure settings unreviewed.

Mitigation: Obtain and review the deployment files before installation, especially container permissions and network exposure.

Risk: The payment helper, external dependencies, and paid package are not fully reviewed.

Mitigation: Verify and pin the payment helper, personally confirm the bill, and inspect the delivered package before running its contents.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/linkkhub-pixiu/skills/linkk-search)
- [Full package service endpoint](https://linkkhub.top)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with shell commands and configuration steps]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Deployment and self-check steps for a local SearXNG instance, with its local base URL for Agent configuration.]

## Skill Version(s):

0.3.8 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
