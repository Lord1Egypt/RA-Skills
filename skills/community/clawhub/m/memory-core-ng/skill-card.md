## Description:

Memory Core NG provides a modular memory system for semantic memory search, memory addition, statistics, and Flomo note import using configurable embeddings and reranking.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jazzqi](https://clawhub.ai/user/jazzqi)

### License/Terms of Use:

MIT

## Use Case:

Developers and OpenClaw users use this skill to add, search, inspect, and import personal or project memories through /memory commands and JavaScript APIs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The artifact includes an exposed API credential.

Mitigation: Replace the distributed key with a user-provided secret from a safe source before use; the publisher should rotate the exposed key and remove it from future artifacts.

Risk: Memory content and search queries are sent to the configured Edgefn embedding and reranking endpoint by default.

Mitigation: Avoid private notes, secrets, business records, or existing memory stores unless external processing is acceptable; prefer local providers or disabling automatic embedding and reranking until clear privacy disclosure and opt-in controls are available.

Risk: Flomo import can process user-selected note export files that may contain sensitive personal content.

Mitigation: Review import files before use and restrict imported content to data that is appropriate for the configured storage and embedding provider.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jazzqi/skills/memory-core-ng)
- [Publisher profile](https://clawhub.ai/user/jazzqi)
- [Artifact README](artifact/README.md)
- [Artifact SKILL.md](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown and JSON-like command responses with JavaScript examples and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Responses may include memory search results, memory records, import summaries, statistics, and setup guidance.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
