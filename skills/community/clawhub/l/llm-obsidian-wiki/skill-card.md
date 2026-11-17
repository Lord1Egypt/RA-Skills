## Description:

Build, maintain, query, archive, and audit a Markdown/Obsidian knowledge wiki that an LLM continuously updates from source materials and prior answers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fengsusky](https://clawhub.ai/user/fengsusky)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to maintain a long-lived personal or team Markdown/Obsidian knowledge base. It helps import source material, compile reusable source/entity/concept/synthesis/comparison/query pages, update indexes and logs, answer questions from the wiki, and run structural audits.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can read and edit files in a target Knowledge vault, which may expose or alter private notes if the workspace scope is too broad.

Mitigation: Run it only against the intended vault and keep private or unrelated directories outside the agent's editable scope.

Risk: Bulk renames, directory migrations, and attachment localization can disrupt links or file organization.

Mitigation: Confirm before bulk operations and rerun the packaged wiki verification script after imports, refactors, renames, or topic-map updates.

Risk: External web sources can introduce unverified or time-sensitive claims into durable wiki pages.

Mitigation: Prefer internal source material, attribute external sources clearly, and separate source viewpoints from externally verified facts.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/fengsusky/skills/llm-obsidian-wiki)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown, wiki files, inline shell commands, and Python audit script output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces or updates local Knowledge vault files and may report audit findings for broken links, index coverage, source coverage, and UTF-8 issues.]

## Skill Version(s):

1.0.2 (source: server release metadata and user changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
