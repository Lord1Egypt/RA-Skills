## Description: <br>
Use this skill when a task involves Knative Serving on Kubernetes, including designing or deploying serverless container workloads, converting Deployments to Knative Services, writing or reviewing serving.knative.dev manifests, using kn or kubectl for Serving resources, configuring autoscaling or scale-to-zero, managing Revisions and traffic splits, debugging Ready/Route/Configuration/Revision failures, configuring cluster-local or custom-domain networking, probes, timeouts, volumes, private registries, observability, or resolving common Serving errors even when the user only mentions ksvc, routes, revisions, canary, cold starts, or Knative autoscaling. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wei840222](https://clawhub.ai/user/wei840222) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and platform engineers use this skill to design, update, troubleshoot, and review Knative Serving workloads on Kubernetes. It helps produce operational guidance, manifests, and commands for services, revisions, traffic, autoscaling, networking, observability, and debugging. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Commands may inspect or change Kubernetes and Knative resources using the user's current cluster credentials. <br>
Mitigation: Review the active kubectl context and namespace before running generated commands, and approve changes before applying them. <br>
Risk: Traffic changes, deletion commands, DomainMapping, log reads, and all-namespace queries can affect availability, exposure, or data access. <br>
Mitigation: Review commands that delete resources, alter traffic, expose domains, read logs, or query all namespaces before execution. <br>
Risk: DomainMapping can expose a private or cluster-local service through a public hostname. <br>
Mitigation: Confirm public exposure is intended before creating or changing DomainMapping resources. <br>


## Reference(s): <br>
- [Overview and CRDs](references/overview-and-crds.md) <br>
- [kn CLI](references/kn-cli.md) <br>
- [Autoscaling](references/autoscaling.md) <br>
- [Container Settings](references/container-settings.md) <br>
- [Revisions and Traffic](references/revisions-and-traffic.md) <br>
- [Networking](references/networking.md) <br>
- [Observability](references/observability.md) <br>
- [Debugging](references/debugging.md) <br>
- [Common Errors](references/common-errors.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/wei840222/knative-serving) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Guidance, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline YAML and bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires kubectl and kn for command execution against a user's Kubernetes cluster.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
