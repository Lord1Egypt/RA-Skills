## Description:

Convert recipe text, transcripts, image descriptions, or other raw recipe content into a .paprikarecipes file for Paprika Recipe Manager.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nogara](https://clawhub.ai/user/nogara)

### License/Terms of Use:


## Use Case:

External users use this skill to turn recipes from pasted text, transcripts, image descriptions, or URL content into Paprika import files while preserving only fields present in the source.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Recipe details may be written to local temporary JSON and .paprikarecipes files during packaging.

Mitigation: Avoid sensitive personal recipe notes or delete temporary JSON and .paprikarecipes files after import.

Risk: The resulting recipe can only reflect fields present in the source content.

Mitigation: Review the delivered field summary and update missing or incorrect recipe details before relying on the import.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/nogara/skills/paprika-recipe-importer)
- [Paprika Recipe Manager](https://www.paprikaapp.com/)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, files, guidance]

**Output Format:** [Markdown guidance with JSON recipe data and a generated .paprikarecipes file]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces Paprika import archives from local temporary JSON recipe files.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
