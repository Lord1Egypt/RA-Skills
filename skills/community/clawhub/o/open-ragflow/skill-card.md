## Description:

RAGFlow open-source Retrieval-Augmented Generation (RAG) engine \u2014 deployment, configuration, management, and troubleshooting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[openlark](https://clawhub.ai/user/openlark)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to deploy, configure, administer, and troubleshoot RAGFlow installations. It also helps users understand RAGFlow architecture and operate datasets, documents, agents, chats, model providers, and REST or CLI workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Deployment commands can change host or container state if executed without review.

Mitigation: Review commands before execution, use a pinned RAGFlow release or commit, and prefer an isolated host or container environment for Docker and source-build work.

Risk: Default service passwords and LLM API keys can expose deployed systems or secrets.

Mitigation: Change default MySQL and MinIO passwords before exposure, and keep API keys out of shell history and version control.

Risk: Destructive commands such as volume removal, dataset drops, or Docker pruning can cause data loss.

Mitigation: Confirm destructive commands before running them and back up important RAGFlow data before cleanup or migration operations.

## Reference(s):

- [RAGFlow website](https://ragflow.io)
- [RAGFlow documentation](https://ragflow.io/docs/dev/)
- [RAGFlow GitHub repository](https://github.com/infiniflow/ragflow)
- [RAGFlow Architecture Reference](references/architecture.md)
- [RAGFlow CLI Reference](references/cli-reference.md)
- [RAGFlow Deployment Reference](references/deployment.md)
- [ClawHub skill page](https://clawhub.ai/openlark/skills/open-ragflow)
- [OpenLark publisher profile](https://clawhub.ai/user/openlark)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration, Code]

**Output Format:** [Markdown with inline shell commands, configuration snippets, CLI examples, and troubleshooting tables]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include Docker Compose commands, CLI statements, REST API paths, and configuration file edits for RAGFlow deployments.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
