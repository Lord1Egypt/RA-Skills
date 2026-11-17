## Description:

Kb Keyword Graph helps agents read a knowledge base keyword tree and summarize its structure, topic distribution, interactive graph view, and keyword relationships.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ywc668](https://clawhub.ai/user/ywc668)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, agents, and knowledge-base users use this skill to inspect a 2brain library or configured corpus by generating structure summaries, topic distributions, keyword relationship explanations, and an optional interactive keyword graph.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A configurable API base can send the base_id and graph API credential to an unintended or non-HTTPS endpoint.

Mitigation: Use only a trusted 2brain API base and avoid setting TWOBRAIN_API_BASE to arbitrary or http URLs.

Risk: The local and Elasticsearch backends expand the skill beyond the primary 2brain-only workflow by reading a configured folder or querying a configured Elasticsearch endpoint.

Mitigation: Enable those backends only when the folder or Elasticsearch endpoint is intentional and trusted.

Risk: The graph API key is sensitive and may be stored in a user config file.

Mitigation: Keep ~/.config/2brain-keyword-map/config.json private, restrict file permissions, and do not paste the token into prompts or artifacts.

Risk: Generated HTML graphs are built from keyword data returned by the selected backend.

Mitigation: Open generated graph files only when the backend and keyword data source are trusted.

## Reference(s):

- [Skill Instructions](artifact/SKILL.md)
- [Execution Workflows](artifact/references/workflows.md)
- [Validation Notes](artifact/references/validation.md)
- [Chinese Skill Instructions](artifact/references/SKILL.zh.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance, files]

**Output Format:** [Markdown guidance with JSON command output and optional self-contained HTML graph files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses a base_id or configured corpus/index; graph percentages are sibling-share values rather than whole-KB percentages.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
