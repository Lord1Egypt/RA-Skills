## Description: <br>
Build, modify, and review Prefect-based offline orchestration for Kubernetes deployments, including flows, tasks, prefect.yaml changes, resource profiles, concurrency, CI alignment, and deployment behavior. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ExenVitor](https://clawhub.ai/user/ExenVitor) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to add, refactor, and review Prefect-managed offline workflows that run through Kubernetes work pools. It helps keep orchestration, deployment configuration, resource sizing, concurrency controls, and validation steps aligned. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Suggested workflow or deployment changes could alter schedules, work pools, resource limits, or Kubernetes Secret and ConfigMap references. <br>
Mitigation: Review generated changes to prefect.yaml, schedules, work pools, resource limits, and Secret or ConfigMap references before deployment. <br>
Risk: Enabling or modifying scheduled Prefect runs before validation could launch unintended work. <br>
Mitigation: Run focused tests and a small manual validation run before enabling or changing schedules. <br>


## Reference(s): <br>
- [Architecture](references/architecture.md) <br>
- [Deployment Patterns](references/deployment-patterns.md) <br>
- [Flow Design](references/flow-design.md) <br>
- [Resources and Concurrency](references/resources-and-concurrency.md) <br>
- [Template prefect.yaml](references/template-prefect-yaml.md) <br>
- [Prefect v3 Tasks](https://docs.prefect.io/v3/concepts/tasks) <br>
- [Prefect v3 Task Runners](https://docs.prefect.io/v3/concepts/task-runners/) <br>
- [Prefect v3 Flows](https://docs.prefect.io/v3/concepts/flows) <br>
- [Prefect v3 Deployments](https://docs.prefect.io/v3/concepts/deployments) <br>
- [Prefect v3 Workers](https://docs.prefect.io/v3/concepts/workers) <br>
- [Prefect v3 Tag-Based Concurrency Limits](https://docs.prefect.io/v3/concepts/tag-based-concurrency-limits) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Configuration] <br>
**Output Format:** [Markdown guidance with code and YAML configuration suggestions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose changes to Prefect flow code, prefect.yaml deployment definitions, Kubernetes resource settings, concurrency policies, and validation steps.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
