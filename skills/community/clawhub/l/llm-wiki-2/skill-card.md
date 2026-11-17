## Description:

LLM Wiki helps an agent incrementally build, maintain, query, and lint a structured Markdown wiki from user-provided source material.

This skill is ready for commercial/non-commercial use.

## Publisher:

[edde-101](https://clawhub.ai/user/edde-101)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, researchers, and knowledge workers use this skill to organize evolving source material into a persistent local Markdown wiki, then query or lint that wiki for cross-linked knowledge, missing pages, stale claims, and contradictions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The agent writes and updates local Markdown files, so an incorrect wiki root could place generated pages in the wrong repository or overwrite expected wiki outputs.

Mitigation: Confirm the wiki root before initialization or ingestion and review planned file writes in important repositories.

Risk: Raw source material may contain sensitive content that should not be exposed through online search or persistent memory.

Mitigation: Keep sensitive raw content offline unless search is explicitly allowed, and store only harmless preferences in memory.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/edde-101/skills/llm-wiki-2)
- [Server-resolved GitHub provenance](https://github.com/Edde-101/SimpleAgent/tree/main/skills/llm-wiki)

## Skill Output:

**Output Type(s):** [Markdown, Files, Guidance, Shell commands]

**Output Format:** [Markdown wiki pages, Markdown reports, status summaries, and optional shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes and updates local wiki, source-summary, index, log, schema, and lint report files under a user-confirmed wiki root.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
