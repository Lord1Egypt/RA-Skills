## Description: <br>
Connect to Kubernetes clusters using YAML configuration files. Use when you need to apply, validate, or manage Kubernetes resources via kubectl with YAML input. Handles kubeconfig creation, context switching, and resource deployment from YAML content. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jokerzeng](https://clawhub.ai/user/jokerzeng) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and platform engineers use this skill to validate Kubernetes YAML, apply manifests, manage kubeconfig files, and switch kubectl contexts for accessible clusters. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: kubectl commands can affect real Kubernetes clusters. <br>
Mitigation: Run dry-runs first, confirm the current context and namespace, and avoid production unless explicitly intended. <br>
Risk: Untrusted manifests can create, modify, or delete cluster resources. <br>
Mitigation: Review manifests before applying them and validate YAML before execution. <br>
Risk: Kubeconfig files can contain credentials or sensitive cluster access details. <br>
Mitigation: Store kubeconfig files with restrictive permissions such as mode 600. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jokerzeng/k8s-yaml-connect) <br>
- [Kubernetes Documentation](https://kubernetes.io/docs/) <br>
- [kubectl Cheat Sheet](https://kubernetes.io/docs/reference/kubectl/cheatsheet/) <br>
- [Kubernetes Configuration Best Practices](https://kubernetes.io/docs/concepts/configuration/overview/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash and YAML code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose kubectl commands and kubeconfig handling steps that should be reviewed before execution against a real cluster.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
