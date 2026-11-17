## Description:

Context engineering platform for AI agents. Upload documents, search with semantic and structured queries, and inject relevant context into LLM prompts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[punithg](https://clawhub.ai/user/punithg)

### License/Terms of Use:


## Use Case:

Developers and agent builders use this skill to integrate Memic document search, database search, RAG context retrieval, and setup guidance into AI agents, copilots, and applications that need grounded context.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill encourages sending documents, database content, and retrieved RAG context to hosted services.

Mitigation: Upload only approved or sanitized documents, avoid secrets and regulated data unless retention and access controls are approved, and use least-privilege read-only database credentials for connectors.

Risk: Retrieved document text may carry prompt-injection content into downstream agents or LLM prompts.

Mitigation: Keep retrieved document text out of system and developer prompts, treat it as untrusted user context, and review generated answers before sensitive use.

Risk: The skill depends on the external memic Python package and a hosted API key.

Mitigation: Use a virtual environment, pin and review the memic package version, and scope MEMIC_API_KEY access to the minimum required project and environment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/punithg/skills/memic)
- [Memic dashboard](https://app.memic.ai)
- [Memic package on PyPI](https://pypi.org/project/memic/)
- [Memic Python SDK repository](https://github.com/memic-ai/memic-python)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown with Python and bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes setup steps, API usage examples, troubleshooting guidance, and integration patterns for Memic-backed RAG and search.]

## Skill Version(s):

1.0.4 (source: server release metadata; artifact frontmatter: 0.3.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
