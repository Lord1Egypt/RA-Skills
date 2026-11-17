## Description: <br>
Provides Kubernetes beginner troubleshooting guidance and best-practice checks for common Pod, Service, Deployment, networking, storage, and security issues. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, platform engineers, and Kubernetes learners use this skill to diagnose common workload issues, review safer configuration patterns, and generate troubleshooting steps for routine K8s problems. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill includes live-cluster kubectl examples that could affect the wrong cluster, namespace, or workload if executed without confirmation. <br>
Mitigation: Require the user to explicitly choose the target cluster, namespace, and command before execution; prefer read-only diagnostics first. <br>
Risk: The requested tool posture includes command execution, and the evidence flags broad agent tools without clear safety boundaries. <br>
Mitigation: Do not let an agent run kubectl, exec into pods, or scale deployments unless the exact command and target environment are approved. <br>
Risk: Troubleshooting guidance may be incomplete for complex Kubernetes environments. <br>
Mitigation: Use the skill as a reference guide, verify recommendations against cluster state, and limit credentials to the intended environment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thcjp/skills/k8s-toolkit-free) <br>
- [Skill homepage](https://skillhub.cn) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline bash and YAML code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include kubectl diagnostics, Kubernetes manifest examples, and manual review recommendations.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
