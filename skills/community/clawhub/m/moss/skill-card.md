## Description:

Documentation and capabilities reference for Moss semantic search.

This skill is ready for commercial/non-commercial use.

## Publisher:

[coderomaster](https://clawhub.ai/user/coderomaster)

### License/Terms of Use:


## Use Case:

Developers and agent builders use this skill to understand Moss SDKs, REST APIs, semantic and hybrid search workflows, index management, document lifecycle operations, credentials, and integration patterns.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: MOSS_PROJECT_KEY is a project access secret used by Moss SDK and REST API requests.

Mitigation: Treat MOSS_PROJECT_KEY as a secret, provide it through secure environment configuration, and avoid exposing it in prompts, logs, code, or shared outputs.

Risk: Moss document and index operations can upload, sync, or delete indexed data.

Mitigation: Only upload or sync documents intended for Moss-managed indexes, confirm target index names and document IDs before delete operations, and review generated API or SDK calls before execution.

Risk: Package installation guidance can alter the local development environment.

Mitigation: Install only the Moss packages needed for the task, preferably pinned to reviewed versions in a virtual environment or lockfile.

## Reference(s):

- [Moss documentation](https://docs.moss.dev)
- [Moss LLM documentation index](https://docs.moss.dev/llms.txt)
- [Moss ClawHub release](https://clawhub.ai/coderomaster/skills/moss)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline code blocks and command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include SDK usage patterns, REST request examples, environment variable setup, package installation commands, and operational guidance for Moss indexes and documents.]

## Skill Version(s):

1.0.3 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
