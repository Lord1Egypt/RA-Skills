## Description: <br>
Provision and manage production-grade databases on Kubernetes using KubeBlocks, including setup, scaling, backup, restore, monitoring, and troubleshooting for common database engines. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[earayu](https://clawhub.ai/user/earayu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and platform engineers use this skill to provision and operate KubeBlocks-managed databases on Kubernetes across relational, NoSQL, streaming, vector, and search workloads. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can produce commands that mutate or delete Kubernetes database resources. <br>
Mitigation: Confirm kubeconfig context, namespace, target cluster, environment, terminationPolicy, and dry-run output before approving apply, delete, uninstall, restore, scale, patch, or expose commands. <br>
Risk: Credential-retrieval workflows may expose database secrets in chat, logs, or shared terminals. <br>
Mitigation: Require explicit approval before credential retrieval and avoid pasting decoded secrets into chat, logs, or shared terminals. <br>
Risk: Database operations can affect production availability or data durability. <br>
Mitigation: Review the generated plan, backups, restore target, and success conditions before executing mutating operations. <br>


## Reference(s): <br>
- [ClawHub Skill Listing](https://clawhub.ai/earayu/kubeblocks-skills) <br>
- [KubeBlocks Official Docs](https://kubeblocks.io/docs/preview/user_docs/overview/introduction) <br>
- [KubeBlocks LLM Doc Index](https://kubeblocks.io/llms-full.txt) <br>
- [KubeBlocks Supported Addons](https://kubeblocks.io/docs/preview/user_docs/overview/supported-addons) <br>
- [KubeBlocks GitHub Repository](https://github.com/apecloud/kubeblocks) <br>
- [Safety Patterns Reference](artifact/references/safety-patterns.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and Kubernetes YAML examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Kubernetes access through kubeconfig and commonly uses kubectl and helm.] <br>

## Skill Version(s): <br>
0.2.0 (source: SKILL.md frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
