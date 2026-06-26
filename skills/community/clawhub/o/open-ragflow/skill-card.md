## Description: <br>
RAGFlow open-source Retrieval-Augmented Generation (RAG) engine — deployment, configuration, management, and troubleshooting. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[openlark](https://clawhub.ai/user/openlark) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to deploy, configure, manage, and troubleshoot RAGFlow self-hosted RAG systems, including Docker services, LLM provider settings, CLI workflows, API usage, and architecture review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Commands that remove Docker volumes can delete RAGFlow deployment data. <br>
Mitigation: Use disposable or test environments when possible, and back up RAGFlow data before running any reset command such as `docker compose down -v`. <br>
Risk: Docker cleanup or deployment commands can affect shared or production hosts. <br>
Mitigation: Review commands before execution and avoid host-wide Docker cleanup unless the impact on other workloads is understood. <br>
Risk: RAGFlow configuration can involve API keys and service passwords. <br>
Mitigation: Protect LLM API keys and service passwords, avoid exposing them in shared logs or commits, and rotate credentials if they are disclosed. <br>
Risk: Deployed services may be reachable over the network if ports are exposed broadly. <br>
Mitigation: Restrict network exposure with firewall, binding, and access-control settings appropriate for the deployment environment. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/openlark/open-ragflow) <br>
- [RAGFlow Deployment Reference](artifact/references/deployment.md) <br>
- [RAGFlow Architecture Reference](artifact/references/architecture.md) <br>
- [RAGFlow CLI Reference](artifact/references/cli-reference.md) <br>
- [RAGFlow documentation](https://ragflow.io/docs/dev/) <br>
- [RAGFlow website](https://ragflow.io) <br>
- [RAGFlow source repository](https://github.com/infiniflow/ragflow) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash, YAML, and command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include deployment steps, configuration snippets, CLI commands, API guidance, architecture notes, and troubleshooting advice.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
