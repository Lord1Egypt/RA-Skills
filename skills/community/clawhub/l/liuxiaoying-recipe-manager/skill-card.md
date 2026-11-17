## Description:

Recipe Manager helps agents record commercial ingredient recipes, manage recipe versions, calculate ingredient costs, retrieve standard ratios, and export recipe data to CSV or Excel.

This skill is ready for commercial/non-commercial use.

## Publisher:

[luzewen](https://clawhub.ai/user/luzewen)

### License/Terms of Use:

MIT-0

## Use Case:

External operators and recipe-focused agents use this skill to store drink and dessert ingredient formulas, retrieve versioned preparation details, calculate per-recipe costs, and export recipe records for business use.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores recipe data in a local file in the user's home directory.

Mitigation: Install only when local recipe storage is acceptable and protect the home directory according to the sensitivity of recipe and cost data.

Risk: The skill can delete saved recipe entries.

Mitigation: Confirm delete requests carefully and keep backups when recipe history is operationally important.

Risk: Exported spreadsheets may contain formula-like values from recipe text without sanitization.

Mitigation: Treat exported CSV or Excel files as untrusted when recipe content may come from other people.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/luzewen/skills/liuxiaoying-recipe-manager)
- [Publisher profile](https://clawhub.ai/user/luzewen)
- [Server-resolved GitHub provenance](https://github.com/luzewen/openclaw-recipe-manager)

## Skill Output:

**Output Type(s):** [text, shell commands, files, configuration]

**Output Format:** [Text responses and JSON command results, with optional CSV or Excel export files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Stores recipe data locally and can create export files in the user's home directory.]

## Skill Version(s):

0.1.0 (source: server release metadata; artifact frontmatter lists 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
