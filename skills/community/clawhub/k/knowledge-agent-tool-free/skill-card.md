## Description:

Helps users capture URLs, videos, articles, social posts, and research notes into a local Markdown knowledge base and retrieve them with the know CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to save web and research material as local knowledge entries, maintain an index, and search or browse prior captures.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks an agent to run a separate know CLI against a persistent local knowledge directory, which may mutate saved content or indexes.

Mitigation: Review proposed know commands before execution, keep backups or version control for the knowledge directory, and confirm the target KNOWLEDGE_DIR before tidy or reindex operations.

Risk: External API behavior and automatic mutating maintenance are under-scoped in the security evidence.

Mitigation: Avoid granting broad SEO/API tasks until the publisher documents the exact commands and external services used.

## Reference(s):


## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell command examples and CLI output summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include know CLI commands, local Markdown knowledge entries, and index maintenance guidance.]

## Skill Version(s):

1.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
