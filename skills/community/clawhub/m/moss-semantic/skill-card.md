## Description:

Documentation and capabilities reference for Moss semantic search APIs, SDKs, and integration patterns.

This skill is ready for commercial/non-commercial use.

## Publisher:

[coderomaster](https://clawhub.ai/user/coderomaster)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to understand Moss semantic search capabilities, SDK methods, authentication, integration patterns, and operational workflows for retrieval-enabled agents.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Moss project credentials could be exposed if copied into logs, prompts, source control, or shared configuration.

Mitigation: Store project keys in a secret manager or protected environment variables and avoid placing credentials in prompts or committed files.

Risk: Documents and user queries sent through retrieval workflows may contain private or sensitive information.

Mitigation: Review document, query, and automatic context-injection flows for privacy requirements before enabling them in an agent.

Risk: Delete operations can remove indexes or documents that may be needed for retention, audit, or recovery.

Mitigation: Confirm backup, retention, and recovery requirements before using index or document deletion workflows.

Risk: Unpinned Moss SDK packages may change behavior over time.

Mitigation: Pin package versions and review dependency updates before deploying the skill in a production agent environment.

## Reference(s):

- [Moss documentation](https://docs.usemoss.dev)
- [Moss LLM documentation index](https://docs.usemoss.dev/llms.txt)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown documentation with tables, code blocks, shell command examples, and concise guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Documentation-only output; no executable artifacts are produced by the skill itself.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
