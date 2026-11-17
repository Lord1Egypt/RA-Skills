## Description:

Hermes Workflow Engine orchestrates multi-step agent workflows with DAG dependencies, parallel execution planning, failover, resource monitoring, version management, pattern detection, dashboards, and community sharing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lgx281227231](https://clawhub.ai/user/lgx281227231)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and automation-focused agent users use this skill to define, validate, plan, and run YAML workflows for repeatable multi-step tasks that may need pausing, resuming, delegation, or parallel work.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad workflow automation can execute or delegate unsafe steps if a workflow is accepted without review.

Mitigation: Validate and inspect workflow plans before execution, review generated shell commands and delegation payloads, and require user approval for creation, execution, rollback, deletion, publishing, and large parallel runs.

Risk: The artifact includes deployment guidance that copies SSH private keys and ClawHub config tokens between machines.

Mitigation: Do not copy private keys or ClawHub config tokens across systems; generate fresh credentials per machine and rotate any credentials that were copied.

Risk: History-based pattern detection and scheduled triggers can read private session history or trigger automation from past behavior.

Mitigation: Disable or tightly scope history scanning and scheduled triggers when session privacy matters, and scrub sensitive session data before enabling pattern detection.

Risk: Imported .tgz workflow packages are handled weakly and should be treated as untrusted until path validation is fixed.

Mitigation: Import only trusted packages after inspecting archive members and metadata, or test imports in a sandboxed workspace before using the workflows.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lgx281227231/skills/hermes-workflow-engine)
- [Workflow YAML Format Specification](scripts/FORMAT.md)
- [ClawHub Publishing Workflow](references/clawhub-publishing.md)
- [Cross-System Deployment: Hermes to OpenClaw](references/cross-system-deployment.md)
- [Workflow Engine Optimization - Darwin 2.0 Cycle](references/darwin-optimization-cycle.md)
- [Darwin Optimization Log](references/darwin-optimization-log.md)
- [Apache Airflow DAGs](https://airflow.apache.org/docs/apache-airflow/stable/core-concepts/dags.html)
- [LangGraph documentation](https://langchain-ai.github.io/langgraph/)
- [Prefect documentation](https://docs.prefect.io/)
- [Temporal documentation](https://docs.temporal.io/)
- [Directed acyclic graph](https://en.wikipedia.org/wiki/Directed_acyclic_graph)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown and JSON-oriented CLI output with YAML workflow configuration and shell command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce execution plans, delegate-task payloads, workflow state files, version metadata, tgz workflow packages, and HTML dashboards.]

## Skill Version(s):

3.1.0 (source: server release evidence; artifact frontmatter says 3.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
