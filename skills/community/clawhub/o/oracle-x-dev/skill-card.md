## Description:

Guides agents extending the Oracle-X financial terminal codebase, including FastAPI endpoints, upstream data sources, blockchain adapters, prompts, LLM-backed notes, and repository-specific test gates.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yigtwxx](https://clawhub.ai/user/yigtwxx)

### License/Terms of Use:

MIT License

## Use Case:

Developers and engineering agents use this skill when modifying the Oracle-X repository so changes follow its endpoint, upstream provider, blockchain adapter, prompt, LLM, and testing conventions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Using this repository-specific skill outside Oracle-X could lead to incorrect engineering choices.

Mitigation: Install and apply it only when working in the Oracle-X codebase, and cross-check local repository documentation before making changes.

Risk: Changes guided by the skill may affect authentication, provider health reporting, external data behavior, or LLM-backed notes if repository conventions are skipped.

Mitigation: Review proposed changes and run the backend, frontend, skill build, and repository facts checks described by the skill before release.

## Reference(s):

- [Oracle-X repository](https://github.com/Yigtwxx/OracleX)
- [Oracle-X agent skill source](https://github.com/Yigtwxx/OracleX/tree/main/agent-skill)
- [Adding a backend endpoint](references/endpoint.md)
- [Adding an upstream data source](references/upstream.md)
- [Adding a blockchain](references/chains.md)
- [Prompts, the model chain, and notes](references/llm.md)
- [Testing](references/testing.md)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, shell commands, configuration]

**Output Format:** [Markdown guidance with inline code and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Repository-specific to Oracle-X; intended for agents working in that codebase.]

## Skill Version(s):

1.0.3 (source: server release metadata; artifact frontmatter reports 1.3.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
