## Description:

LLM-Wiki-skills helps an agent initialize, ingest, query, lint, and maintain a persistent Markdown wiki following the LLM Wiki pattern.

This skill is ready for commercial/non-commercial use.

## Publisher:

[1knownothing](https://clawhub.ai/user/1knownothing)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and knowledge workers use this skill set to build and maintain local research, reading, team, or personal knowledge wikis with source summaries, cross-references, health checks, and cited query answers.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad triggers and persistent wiki writes could cause unexpected changes to local knowledge-base files.

Mitigation: Restrict the skill to a specific wiki directory and require confirmation before creating or editing files.

Risk: Broad shell access can expand the impact of a wiki maintenance workflow beyond normal Markdown editing.

Mitigation: Remove or avoid Bash access unless a specific shell-only workflow is approved.

Risk: Ingest and query workflows may add incorrect, stale, or poorly sourced claims to a persistent wiki.

Mitigation: Review generated summaries, citations, contradiction notes, and log entries before treating them as trusted knowledge.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/1knownothing/skills/llm-wiki-skills)
- [Obsidian cloud sync guide](https://www.bilibili.com/video/BV1fZCyBYEuT/?spm_id_from=333.788.top_right_bar_window_history.content.click&vd_source=2c231d5b43d9ccf0848317adb47c0383)
- [The Assistant Axis](https://www.anthropic.com/research/assistant-axis)
- [Toy Models of Superposition](https://transformer-circuits.pub/2022/toy_model/index.html)
- [Scaling Monosemanticity](https://transformer-circuits.pub/2024/scaling-monosemanticity/index.html)
- [Circuit Tracing](https://transformer-circuits.pub/2025/attribution-graphs/methods.html)
- [On the Biology of a Large Language Model](https://transformer-circuits.pub/2025/attribution-graphs/biology.html)
- [Activation Oracles](https://arxiv.org/pdf/2512.15674)
- [When the Coffee Feature Activates on Coffins](https://arxiv.org/pdf/2601.03047)

## Skill Output:

**Output Type(s):** [text, markdown, files, shell commands, configuration, guidance]

**Output Format:** [Markdown wiki pages, tables, slide decks, shell command suggestions, and concise status summaries.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update persistent local wiki files, including index.md, log.md, schema files, source summaries, concept pages, entity pages, and synthesized query pages.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
