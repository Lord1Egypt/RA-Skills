## Description: <br>
Converts recipe text, transcripts, image descriptions, or other raw content into a .paprikarecipes import file for Paprika Recipe Manager. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nogara](https://clawhub.ai/user/nogara) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and agent operators use this skill to convert recipe content from pasted text, transcripts, image descriptions, or URL content into Paprika import files. The skill is intended to preserve only recipe fields present in the source and report which fields were found or absent. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Recipe-derived filenames and shared temporary paths can expose source titles, collide with existing files, or create unsafe shell paths. <br>
Mitigation: Use sanitized fixed filenames or a private temporary directory, quote paths, and remove intermediate JSON files after creating the `.paprikarecipes` archive. <br>
Risk: The skill creates local recipe files and runs a local Python packaging script. <br>
Mitigation: Review the extracted recipe JSON and destination path before running the script, and only install the skill if local file creation is acceptable. <br>


## Reference(s): <br>
- [Paprika Recipe Manager](https://www.paprikaapp.com/) <br>
- [ClawHub skill page](https://clawhub.ai/nogara/paprika-recipe-importer) <br>


## Skill Output: <br>
**Output Type(s):** [Files, JSON, Shell commands, Guidance] <br>
**Output Format:** [.paprikarecipes archive with concise Markdown guidance and a field coverage summary] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates local JSON intermediates and a Paprika import archive; supports a single recipe object or an array of recipes.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
