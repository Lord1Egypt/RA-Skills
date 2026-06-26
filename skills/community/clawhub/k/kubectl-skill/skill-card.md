## Description: <br>
Provides detailed kubectl command references for managing Kubernetes resources, cluster information, logs, debugging, context switching, and advanced operations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xpdd](https://clawhub.ai/user/xpdd) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and platform engineers use this skill as a static kubectl reference for Kubernetes resource management, command syntax lookup, cluster inspection, logging, debugging, and context management. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Some generated reference pages may include unrelated database or storage options. <br>
Mitigation: Check command flags against kubectl --help or official Kubernetes documentation before using them. <br>
Risk: Some examples may expose credentials or sensitive cluster information. <br>
Mitigation: Avoid sharing outputs containing secrets, command-line passwords, kubeconfig data, service account tokens, or cluster endpoints. <br>
Risk: Mutating kubectl commands can change or disrupt Kubernetes clusters. <br>
Mitigation: Review delete, apply, certificate approval, RBAC, exec, kubeconfig, and profile-editing commands before running them against a live cluster. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/xpdd/kubectl-skill) <br>
- [Publisher profile](https://clawhub.ai/user/xpdd) <br>
- [Kubernetes kubectl reference](artifact/_index.md) <br>
- [kubectl quick reference](artifact/quick-reference.md) <br>
- [kubectl JSONPath support](artifact/jsonpath.md) <br>
- [kubectl commands](artifact/generated/kubectl.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown reference material with inline shell commands and command option tables] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Static reference content; users should verify generated command options against kubectl --help or official Kubernetes documentation before use.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
