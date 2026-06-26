## Description: <br>
Alibaba Cloud STS helps agents operate Alibaba Cloud STS through an OOMOL-connected account and the oo CLI instead of calling the API directly. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to request Alibaba Cloud STS temporary credentials through an OOMOL-connected account. It supports role assumption and OIDC federation workflows while using the live connector schema before action execution. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can generate Alibaba Cloud temporary credentials through the connected account. <br>
Mitigation: Treat connector outputs as secrets and avoid exposing or persisting returned credentials unnecessarily. <br>
Risk: Credential-generating actions may be presented as safe read-style operations. <br>
Mitigation: Verify the requested role, scope, action, and payload before using returned credentials. <br>
Risk: Setup guidance includes pipe-to-shell installation commands for the oo CLI. <br>
Mitigation: Prefer a verified oo CLI installation method and only run setup after an auth or connection failure requires it. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/oomol/oo-aliyun-sts) <br>
- [Publisher profile](https://clawhub.ai/user/oomol) <br>
- [Alibaba Cloud STS homepage](https://www.alibabacloud.com/product/ram) <br>
- [oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [oo CLI install guide](https://cli.oomol.com/install-guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON payload examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Connector responses may include temporary credential data and an execution id.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata and skill metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
