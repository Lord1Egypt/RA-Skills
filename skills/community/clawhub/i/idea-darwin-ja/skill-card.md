## Description:

Idea Darwin 日本語版 is a Japanese-language workflow that turns raw ideas into structured idea cards and iteratively refines them through scoring, deepening, variation, crossing, and round reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jianyangzhai](https://clawhub.ai/user/jianyangzhai)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to run a local Japanese-language idea incubation workflow that parses an ideas file, creates structured cards, scores and evolves ideas across rounds, and produces status, leaderboard, and round summaries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated idea cards, scores, reports, and recommendations may contain incomplete or misleading guidance.

Mitigation: Review generated project files and user-facing summaries before relying on them for planning or execution.

Risk: The workflow writes and updates local notes under the current project directory.

Mitigation: Run it only in the intended workspace and review changed files before keeping or sharing them.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/jianyangzhai/skills/idea-darwin-ja)
- [Idea Darwin Homepage](https://github.com/warmskull/idea-darwin)
- [Action Reference](artifact/references/actions.md)
- [Prompt Templates](artifact/references/prompts.md)
- [Idea Card Template](artifact/assets/card-template.md)

## Skill Output:

**Output Type(s):** [markdown, json, configuration, guidance]

**Output Format:** [Markdown project notes, YAML configuration, JSON relationship graph files, and conversational summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates and updates local project files such as idea cards, round reports, leaderboards, configuration, stimuli, and relation graphs.]

## Skill Version(s):

1.0.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
