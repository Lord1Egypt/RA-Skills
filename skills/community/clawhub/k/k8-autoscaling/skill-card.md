## Description: <br>
Configure Kubernetes autoscaling with HPA, VPA, and KEDA. Use for horizontal/vertical pod autoscaling, event-driven scaling, and capacity management. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rohitg00](https://clawhub.ai/user/rohitg00) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and platform engineers use this skill to design, review, and troubleshoot Kubernetes autoscaling with HPA, VPA, and KEDA. It helps produce autoscaling manifests, command-oriented checks, and configuration guidance for capacity management and event-driven scaling. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated Kubernetes manifests or commands could target the wrong cluster, namespace, or workload. <br>
Mitigation: Confirm the active cluster context, namespace, and target deployment before applying generated YAML or running operational commands. <br>
Risk: Autoscaling settings could cause unexpected cost, availability, or cold-start behavior. <br>
Mitigation: Review min and max replicas, scale-to-zero behavior, trigger thresholds, and rollback plans before production use. <br>


## Reference(s): <br>
- [KEDA Trigger Reference](artifact/KEDA-TRIGGERS.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/rohitg00/k8-autoscaling) <br>
- [Publisher Profile](https://clawhub.ai/user/rohitg00) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown with YAML and command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces Kubernetes autoscaling guidance and manifest examples for human review before cluster application.] <br>

## Skill Version(s): <br>
1.0.0 (source: server evidence release.version) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
