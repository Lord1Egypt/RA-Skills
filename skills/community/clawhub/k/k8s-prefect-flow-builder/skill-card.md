## Description:

Build, modify, and review Prefect-based offline orchestration in this repository.

This skill is ready for commercial/non-commercial use.

## Publisher:

[exenvitor](https://clawhub.ai/user/exenvitor)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to add, modify, or review Prefect v3 offline workflows, deployment configuration, resource profiles, concurrency controls, and Kubernetes execution settings.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated Prefect deployment changes can alter schedules, work-pool routing, resource limits, concurrency policies, or Kubernetes secret references.

Mitigation: Review prefect.yaml, schedules, work-pool names, resource limits, and Kubernetes secret references before applying output, then run a small manual validation before enabling scheduled runs.

Risk: Incorrect flow, task, or child-flow boundaries can hide failures or overload shared infrastructure.

Mitigation: Keep orchestration separate from business logic, raise exceptions for failed work, use the appropriate concurrency layer, and run focused tests for changed flow and job code.

## Reference(s):

- [Architecture](references/architecture.md)
- [Deployment Patterns](references/deployment-patterns.md)
- [Flow Design](references/flow-design.md)
- [Resources and Concurrency](references/resources-and-concurrency.md)
- [Template prefect.yaml](references/template-prefect-yaml.md)
- [Prefect v3 Tasks](https://docs.prefect.io/v3/concepts/tasks)
- [Prefect v3 Task Runners](https://docs.prefect.io/v3/concepts/task-runners/)
- [Prefect v3 Flows](https://docs.prefect.io/v3/concepts/flows)
- [Prefect v3 Deployments](https://docs.prefect.io/v3/concepts/deployments)
- [Prefect v3 Workers](https://docs.prefect.io/v3/concepts/workers)
- [Prefect v3 Tag-Based Concurrency Limits](https://docs.prefect.io/v3/concepts/tag-based-concurrency-limits)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown with code, YAML, and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
