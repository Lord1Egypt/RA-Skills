## Description: <br>
Hermes Workflow Engine orchestrates goal-driven multi-step workflows with DAG dependencies, parallel execution, failover, resource monitoring, version management, pattern detection, dashboards, and community sharing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lgx281227231](https://clawhub.ai/user/lgx281227231) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to define, validate, plan, and execute reusable YAML workflows for repetitive or long-running multi-step tasks that need dependency ordering, retries, pause/resume, dashboards, or version management. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can orchestrate shell commands, subagents, and workflow steps that affect local files or external services. <br>
Mitigation: Review each workflow, run validation and planning first, and execute only in an environment with appropriate permissions and resource limits. <br>
Risk: The artifact includes guidance for copying private keys or ClawHub tokens between machines. <br>
Mitigation: Do not follow credential-copy instructions; use freshly generated, scoped credentials and standard secret-management practices. <br>
Risk: Automatic trigger and session-history scanning features may inspect prior activity or propose workflows without an explicit command. <br>
Mitigation: Disable or avoid history-based and automatic trigger features unless the operator explicitly wants that behavior. <br>
Risk: Community archive import can introduce untrusted workflow content. <br>
Mitigation: Avoid importing untrusted community archives; inspect archives and workflow YAML before installation or execution. <br>


## Reference(s): <br>
- [Hermes Workflow Engine on ClawHub](https://clawhub.ai/lgx281227231/hermes-workflow-engine) <br>
- [Workflow YAML Format Specification](scripts/FORMAT.md) <br>
- [Cross-System Deployment Guide](references/cross-system-deployment.md) <br>
- [Cross-Server Deployment Guide](references/cross-server-deployment.md) <br>
- [ClawHub Publishing Workflow](references/clawhub-publishing.md) <br>
- [Apache Airflow DAG Concepts](https://airflow.apache.org/docs/apache-airflow/stable/core-concepts/dags.html) <br>
- [LangGraph Documentation](https://langchain-ai.github.io/langgraph/) <br>
- [Prefect Documentation](https://docs.prefect.io/) <br>
- [Temporal Documentation](https://docs.temporal.io/) <br>
- [Directed Acyclic Graph](https://en.wikipedia.org/wiki/Directed_acyclic_graph) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with YAML snippets, Python CLI commands, and generated workflow, run, archive, or dashboard files when executed.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Workflow execution may create local state, run logs, community archives, and HTML dashboards through the bundled scripts.] <br>

## Skill Version(s): <br>
3.1.0 (source: server release metadata; artifact frontmatter reports 3.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
