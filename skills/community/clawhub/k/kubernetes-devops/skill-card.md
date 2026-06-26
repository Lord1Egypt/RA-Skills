## Description: <br>
Kubernetes manifest generation for Deployments, StatefulSets, CronJobs, Services, Ingresses, ConfigMaps, Secrets, and PVCs with production-grade security and health checks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wpank](https://clawhub.ai/user/wpank) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and DevOps engineers use this skill to create and review Kubernetes YAML for application workloads, networking, configuration, secrets, storage, and multi-environment deployment organization. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated LoadBalancer or Ingress examples could expose services publicly if copied without environment-specific review. <br>
Mitigation: Review each external exposure path before applying manifests, and use source restrictions, TLS, authentication, and network policies where appropriate. <br>
Risk: Placeholder secrets or configuration examples could be committed or applied without replacement. <br>
Mitigation: Replace placeholders, keep real secrets out of Git, and use a secret manager or sealed/external secret workflow for sensitive values. <br>


## Reference(s): <br>
- [Kubernetes skill page](https://clawhub.ai/wpank/kubernetes-devops) <br>
- [Deployment specification reference](references/deployment-spec.md) <br>
- [Service specification reference](references/service-spec.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Code, Shell commands, Configuration instructions] <br>
**Output Format:** [Markdown with YAML and bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces Kubernetes manifest examples and validation guidance that should be reviewed before applying to a cluster.] <br>

## Skill Version(s): <br>
1.0.0 (source: SKILL.md frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
