## Description:

Markdown Memory helps an agent maintain local, human-readable memory using Markdown files, SQLite-backed vector search, and Ollama embeddings.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kk-kingkong](https://clawhub.ai/user/kk-kingkong)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to give an agent local cross-session memory, including daily notes, long-term preferences, session history, and semantic memory search.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent local memory can affect future agent behavior without enough user control.

Mitigation: Define what may be saved, avoid sensitive personal or credential data, and provide a clear way to inspect, edit, delete, and roll back saved entries.

Risk: Loading memory, personality, user, and AGENTS.md content can mix user data with behavior-shaping instructions.

Mitigation: Keep memories separate from agent policy and personality instructions, and review memory content before reusing it across sessions.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/kk-kingkong/skills/markdown-memory)
- [Publisher profile](https://clawhub.ai/user/kk-kingkong)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell and Python command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local memory file conventions and optional vector-search workflow guidance.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
