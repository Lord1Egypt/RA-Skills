## Description:

Idea Darwin is an automated idea iteration system that imports raw ideas, structures them into scored cards, and runs rounds of deepening, derivation, crossbreeding, critique, and validation to surface stronger concepts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jianyangzhai](https://clawhub.ai/user/jianyangzhai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, creators, and product teams use this skill to turn an ideas.md file into a managed idea pool with scored cards, round reports, rankings, and next-step recommendations. It supports structured brainstorming workflows where ideas are iterated, compared, crossed, critiqued, and validated over repeated rounds.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill creates and updates local idea-project state in the current workspace.

Mitigation: Install and run it only where local project files may be created or modified, and review generated files before running multiple rounds.

Risk: The skill reads idea documents and may be exposed to prompt-injection content in untrusted or shared idea files.

Mitigation: Use trusted idea files and avoid shared or untrusted documents until prompt-injection boundaries are strengthened.

Risk: Broad trigger phrases can cause the skill to activate for general brainstorming and idea-ranking requests.

Mitigation: Confirm the intended workspace and requested command before allowing the skill to initialize or update project state.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/jianyangzhai/skills/idea-darwin)
- [Project Homepage](https://github.com/warmskull/idea-darwin)
- [Actions Reference](artifact/references/actions.md)
- [Prompt Templates](artifact/references/prompts.md)
- [Idea Card Template](artifact/assets/card-template.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown reports, YAML/JSON-style project state, structured idea cards, and concise conversational briefings]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates and updates local workspace files including config, idea cards, round reports, leaderboards, stimuli entries, and relationship graphs.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
