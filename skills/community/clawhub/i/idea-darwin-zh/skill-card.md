## Description:

Idea Darwin 中文版 helps agents turn ideas from local project files into structured, scored cards and run iterative rounds of deepening, branching, crossing, critique, validation, and reporting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jianyangzhai](https://clawhub.ai/user/jianyangzhai)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this Chinese-language skill to manage an idea pool in local workspace files, score ideas across defined dimensions, and produce structured iteration reports that support human decisions about which concepts to continue, combine, or pause.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill creates and updates project-local idea cards, reports, configuration, and graph data.

Mitigation: Use it in a workspace where those file changes are expected, and review generated files before relying on them for planning decisions.

Risk: Idea scores, critiques, validation outcomes, and next-step recommendations may be incomplete or subjective.

Mitigation: Treat generated rankings and recommendations as decision support; keep the documented human review step before pausing, merging, or advancing ideas.

## Reference(s):

- [Idea Darwin homepage](https://github.com/warmskull/idea-darwin)
- [Card template](assets/card-template.md)
- [Standard actions reference](references/actions.md)
- [Prompt templates](references/prompts.md)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown reports, Markdown idea cards, YAML configuration, JSON graph data, and concise conversational summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates and updates project-local idea-management files such as cards, round reports, leaderboard reports, config.yaml, stimuli.md, and graph relations.]

## Skill Version(s):

1.0.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
