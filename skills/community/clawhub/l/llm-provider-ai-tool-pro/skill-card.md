## Description:

An agent skill for managing llm-provider API workflows for teams and enterprises, including batch jobs, fine-tuning, evaluations, vector stores, video generation, containers, audit logging, and team permission workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

External developers, automation teams, and enterprise operators use this skill to guide agent-assisted llm-provider API setup and account workflows for batch processing, fine-tuning, evaluations, vector-store RAG, and team-oriented operations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security evidence marks the release suspicious because provider identity and execution scope are broad.

Mitigation: Review the skill before installation and verify that api.llm-provider.com is the intended trusted provider.

Risk: The skill can guide agents toward account-changing API operations such as create, update, delete, upload, fine-tune, batch, and vector-store workflows.

Mitigation: Require explicit previews and human approval before any credentialed or state-changing operation.

Risk: The skill relies on OPENAI_API_KEY-like credentials for API access.

Mitigation: Provide credentials through environment variables or a secrets manager and avoid exposing keys in prompts, files, logs, or generated output.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/llm-provider-ai-tool-pro)
- [Publisher profile](https://clawhub.ai/user/thcjp)
- [llm-provider models endpoint](https://api.llm-provider.com/v1/models)
- [llm-provider files endpoint](https://api.llm-provider.com/v1/files)
- [llm-provider fine-tuning checkpoints endpoint](https://api.llm-provider.com/v1/fine_tuning/jobs/ftjob-abc/checkpoints)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with JSON, Python, and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose API calls, local file operations, and account-changing workflows that require credentialed execution.]

## Skill Version(s):

1.0.0 (source: server release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
