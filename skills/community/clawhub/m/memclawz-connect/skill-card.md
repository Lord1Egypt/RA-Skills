## Description:

Connects AI agents to the MemClawz shared memory bus so they can search prior context before work and write task outcomes back through a simple HTTP API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yoniassia](https://clawhub.ai/user/yoniassia)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to connect agents to a MemClawz memory service, search shared memory before starting tasks, and record completed work for recall across sessions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill documents shared-memory use through unauthenticated or plaintext HTTP service patterns.

Mitigation: Install only for MemClawz services you control, and require authentication, HTTPS or private networking, and project isolation for private work.

Risk: Agents may write sensitive task details into shared memory that persists across sessions.

Mitigation: Redact secrets and private project data, and require explicit approval before writing sensitive summaries.

Risk: Broad automatic memory reads and writes can expose agents to stale, irrelevant, or untrusted context.

Mitigation: Review retrieved memories before relying on them and limit write-backs to concise, factual task summaries.

## Reference(s):

- [MemClawz Connect on ClawHub](https://clawhub.ai/yoniassia/skills/memclawz-connect)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes environment variables, curl requests, memory type labels, and AGENTS.md integration text.]

## Skill Version(s):

1.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
