## Description:

Neta API research and recommendation skill that provides keyword, tag, and category suggestions, validates taxonomy paths, and powers multi-mode content feeds for progressive exploration from broad topics to precise filters.

This skill is ready for commercial/non-commercial use.

## Publisher:

[huxiuhan](https://clawhub.ai/user/huxiuhan)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to research Neta topics, discover keywords, tags, and categories, validate taxonomy paths, and retrieve recommendation, search, or exact content feeds before creation or community interaction.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill directs installation of a mutable global Neta CLI package, which can change behavior after review.

Mitigation: Prefer a pinned, reviewed package version and a project-local install before using generated commands.

Risk: The skill requires NETA_TOKEN, which could be exposed if stored globally or logged.

Mitigation: Scope NETA_TOKEN to the minimum permissions, keep it out of logs, and inject it only for trusted sessions.

Risk: The skill is intended for Neta content discovery and may be misapplied to general web trends or open-ended brainstorming outside its data source.

Mitigation: Use it only for Neta content discovery, taxonomy validation, and Neta feed filtering.

## Reference(s):

- [Neta Suggest ClawHub Skill Page](https://clawhub.ai/huxiuhan/skills/neta-suggest)
- [huxiuhan ClawHub Publisher Profile](https://clawhub.ai/user/huxiuhan)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires NETA_TOKEN and the neta-cli package; command outputs are JSON from the Neta CLI.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
