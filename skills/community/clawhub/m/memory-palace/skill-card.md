## Description:

Memory Palace gives OpenClaw agents persistent memory management for user preferences, project state, reusable experience, semantic search, and time reasoning.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lanzhou3](https://clawhub.ai/user/lanzhou3)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to let an agent store, retrieve, update, summarize, and search long-term memories such as preferences, project status, technical decisions, and reusable lessons.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores long-term local memories that may contain personal, sensitive, or regulated data.

Mitigation: Avoid saving secrets or regulated personal data, and review stored memories and retention behavior before use.

Risk: LLM-enhanced operations may send memory content to configured model endpoints.

Mitigation: Disable LLM-enhanced operations or configure them only with provider endpoints trusted for the data being processed.

Risk: Optional Python setup and vector-search model downloads add dependency and supply-chain exposure.

Mitigation: Avoid the optional postinstall Python setup until dependencies and model sources are pinned and reviewed.

Risk: Security evidence reports unsafe memory ID file handling.

Mitigation: Fix the path traversal issue before broad deployment, and constrain memory IDs and storage paths during review.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/lanzhou3/skills/memory-palace)
- [API Reference](artifact/references/api-reference.md)
- [Architecture](artifact/references/architecture.md)
- [Usage Examples](artifact/references/usage-examples.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown-backed memory files and JSON-like tool responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Stores long-term local memories; optional semantic search and LLM summarization can enrich retrieval results.]

## Skill Version(s):

1.8.5 (source: evidence.release.version, package.json, CHANGELOG released 2026-04-08)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
