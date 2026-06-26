## Description: <br>
Hermes Agent Feishu Bot local deployment guide for WebSocket mode, including Kimi API setup, Feishu permissions, environment variables, group chat policy, and troubleshooting. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cindypapa](https://clawhub.ai/user/cindypapa) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to configure and run a Hermes Agent Feishu Bot locally without a public domain. It helps set up Feishu app credentials, Kimi API access, WebSocket mode, group chat behavior, and basic verification commands. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The setup guidance uses a remote shell installer and local credential storage for API keys and Feishu secrets. <br>
Mitigation: Review the installer before running it, prefer pinned releases or checksums, and store credentials only in a private git-ignored file or secret manager. <br>
Risk: The guide configures group chat behavior and can allow broad responses to group mentions. <br>
Mitigation: Use the documented allowlist or disabled group policy when broad group responses are not intended, and verify Feishu permissions before deployment. <br>


## Reference(s): <br>
- [Hermes official documentation](https://hermes-agent.nousresearch.com) <br>
- [Feishu Open Platform](https://open.feishu.cn) <br>
- [ClawHub skill page](https://clawhub.ai/cindypapa/hermes-feishu-guide) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown with inline bash and environment-variable code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces deployment guidance for local Feishu WebSocket setup and credential configuration; it does not run commands itself.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
