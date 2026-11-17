## Description:

Memory Anchor gives OpenClaw agents durable long-term memory using SQLite hybrid recall, raw and curated anchors, session briefings, and optional LLM embeddings.

This skill is ready for commercial/non-commercial use.

## Publisher:

[g00siferdev-py](https://clawhub.ai/user/g00siferdev-py)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use Memory Anchor to let OpenClaw agents store durable facts and recall preferences, projects, and prior conversations across sessions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can cause an agent to retain broad conversation content as long-term memory.

Mitigation: Confirm the SQLite database location, retention expectations, inspection process, and deletion process before enabling memory capture.

Risk: Setup behavior can install Ollama, start local services, pull embedding models, or use cloud embedding providers.

Mitigation: Require explicit approval before setup or provider changes, and verify whether embeddings stay local or use configured cloud credentials.

## Reference(s):

- [Server-resolved GitHub source repository](https://github.com/g00siferdev-py/Memory-Anchor-OpenClaw)
- [ClawHub skill listing](https://clawhub.ai/g00siferdev-py/skills/memory-anchor-openclaw-2)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON-capable CLI examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Python 3 and SQLite FTS5; optional embedding behavior is configured through local or cloud provider environment variables.]

## Skill Version(s):

0.1.0 (source: server release metadata; artifact frontmatter says 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
