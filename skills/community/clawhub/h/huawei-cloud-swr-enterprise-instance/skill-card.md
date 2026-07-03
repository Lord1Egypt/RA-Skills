## Description: <br>
Huawei Cloud SWR enterprise instance lifecycle management via hcloud CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pintudeyudi](https://clawhub.ai/user/pintudeyudi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and cloud operators use this skill to manage Huawei Cloud SWR enterprise registry resources, including instances, namespaces, registries, repositories, artifacts, credentials, endpoints, domains, and verification workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide changes to powerful cloud registry permissions and resources. <br>
Mitigation: Use least-privilege IAM policies where possible and require explicit human confirmation before creating, updating, or deleting SWR resources. <br>
Risk: Broad public access settings can expose registries or artifacts. <br>
Mitigation: Avoid public 0.0.0.0/0 access and use narrow IP allowlists or private VPC endpoints for registry access. <br>
Risk: Huawei Cloud AK/SK credentials and registry secrets can be exposed through command lines, logs, or conversation text. <br>
Mitigation: Use environment variables or secure configuration, avoid printing secrets, and do not pass real secrets directly in command arguments. <br>
Risk: Insecure registry or TLS settings can weaken transport and registry trust. <br>
Mitigation: Prefer validated TLS, avoid insecure registry options unless explicitly required, and review certificate and domain configuration before use. <br>


## Reference(s): <br>
- [Command Reference](references/command-reference.md) <br>
- [IAM Permission Policies](references/iam-policies.md) <br>
- [SWR Instance API Guide](references/swr-instance-api-guide.md) <br>
- [Verification Method](references/verification-method.md) <br>
- [Huawei Cloud SWR Documentation](https://support.huaweicloud.com/swr/index.html) <br>
- [Huawei Cloud API Explorer](https://apiexplorer.developer.huaweicloud.com/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples, Python helper invocations, and JSON configuration examples.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include Huawei Cloud region settings, IAM policy examples, credential-handling guidance, and confirmation steps for destructive operations.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
