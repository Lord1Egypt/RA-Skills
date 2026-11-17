## Description:

Cognitive memory engine for AI agents that gives OpenClaw and Hermes long-term local memory using compound-cue scoring, Markdown storage, and recall/search/profile/todo commands without LLM APIs, vector databases, or embedding models.

This skill is ready for commercial/non-commercial use.

## Publisher:

[elonaug7](https://clawhub.ai/user/elonaug7)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to add persistent, local, cross-session memory to OpenClaw or Hermes agents for recalling user facts, preferences, decisions, conversation history, profiles, and todos.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can persist conversation-derived memory locally, which may include sensitive user facts or records.

Mitigation: Avoid storing secrets or sensitive records unless the local Markdown memory files can be inspected, edited, and erased under an approved retention process.

Risk: Installation may alter agent instruction files and configure Hermes-related paths or hooks.

Mitigation: Review the installer and upstream repository at a pinned commit, then install in a controlled workspace and inspect changed instruction and hook files before use.

Risk: The skill runs a local Web UI as part of its workflow.

Mitigation: Keep the UI bound to localhost, avoid exposing it on shared networks, and disable it when it is not needed.

## Reference(s):

- [Architecture](references/architecture.md)
- [Benchmark Methodology](references/benchmark.md)
- [Hermes Adapter](references/hermes.md)
- [ClawHub skill page](https://clawhub.ai/elonaug7/skills/mnemosyne)
- [Publisher profile](https://clawhub.ai/user/elonaug7)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON or Markdown memory file references]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local memory recall guidance and configuration steps; no token cap is stated in the evidence.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
