## Description:

Memory Hybrid Stack helps agents read and write a local hybrid memory stack spanning Postgres facts, Redis realtime state, and Qdrant vector recall.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vegabai](https://clawhub.ai/user/vegabai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to connect an assistant to a local memory stack for durable facts, short-lived state, and semantic recall. It provides shell helpers and schema guidance for Postgres, Redis, and Qdrant operations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The helper scripts can write to or delete from local Postgres, Redis, and Qdrant memory stores.

Mitigation: Review mutating SQL, Redis, and Qdrant calls before execution, and use least-privilege accounts for each store.

Risk: The scripts source a memory-stack .env file and may expose or misuse trusted local configuration if that file is unsafe.

Mitigation: Install only with a trusted .env file, keep endpoints pointed at the intended local services, and harden credential loading before production use.

## Reference(s):

- [Hybrid Memory Stack Connections](references/connection-map.md)
- [Memory Hybrid Stack release page](https://clawhub.ai/vegabai/skills/memory-hybrid-stack)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, Code]

**Output Format:** [Markdown with inline bash, SQL, and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May invoke local Postgres, Redis, and Qdrant helper scripts when the required memory stack environment is configured.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
