## Description:

Use this skill when a task involves Knative Serving on Kubernetes, including designing or deploying serverless container workloads, converting Deployments to Knative Services, writing or reviewing serving.knative.dev manifests, using kn or kubectl for Serving resources, configuring autoscaling or scale-to-zero, managing Revisions and traffic splits, debugging Ready/Route/Configuration/Revision failures, configuring cluster-local or custom-domain networking, probes, timeouts, volumes, private registries, observability, or resolving common Serving errors even when the user only mentions ksvc, routes, revisions, canary, cold starts, or Knative autoscaling.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wei840222](https://clawhub.ai/user/wei840222)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and platform engineers use this skill to deploy, convert, configure, and troubleshoot Knative Serving services on Kubernetes. It supports operational work with Services, Revisions, traffic splits, autoscaling, networking, observability, container settings, and common Serving failure modes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The kn CLI install guidance includes an unpinned container image with Kubernetes credentials mounted read-write.

Mitigation: Use a pinned official kn release locally, or run a fixed-version container image by digest with kubeconfig mounted read-only.

Risk: Kubernetes commands may act against a powerful default context.

Mitigation: Use a dedicated least-privileged kubeconfig and confirm the active context before applying commands or manifests.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/wei840222/skills/knative-serving)
- [Publisher Profile](https://clawhub.ai/user/wei840222)
- [Overview and CRDs](references/overview-and-crds.md)
- [kn CLI](references/kn-cli.md)
- [Autoscaling](references/autoscaling.md)
- [Container Settings](references/container-settings.md)
- [Revisions and Traffic](references/revisions-and-traffic.md)
- [Networking](references/networking.md)
- [Observability](references/observability.md)
- [Debugging](references/debugging.md)
- [Common Errors](references/common-errors.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline YAML and bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose kubectl, kn, YAML manifest, and troubleshooting steps for the user's Kubernetes context.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
