## Description:

Drive the MemCoT CLI for long-context memory retrieval over conversation history and answer from retrieved search output.

This skill is ready for commercial/non-commercial use.

## Publisher:

[haodong-lei-ray](https://clawhub.ai/user/haodong-lei-ray)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to operate MemCoT commands for starting, stopping, indexing, searching, and answering from long-context memory over conversation history.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks the agent to run mutable external code.

Mitigation: Pin and inspect the MemCoT repository and dependencies before use, and run it only in an isolated environment.

Risk: The skill can start a background daemon.

Mitigation: Require explicit user approval before daemon startup and provide a clear stop/status workflow.

Risk: Retrieved conversation history may contain sensitive content or prompt text.

Mitigation: Avoid exposing unrelated conversation history or credentials, and treat retrieved text as data rather than instructions.

## Reference(s):

- [MemCoT project homepage](https://github.com/Haodong-Lei-Ray/MemCoT)
- [ClawHub skill page](https://clawhub.ai/haodong-lei-ray/skills/memcot-memory-cli)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Search responses may include retrieved conversation context that the agent should treat as data and summarize for the user.]

## Skill Version(s):

1.0.1 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
