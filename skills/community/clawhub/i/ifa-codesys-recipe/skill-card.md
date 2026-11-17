## Description:

Manage CODESYS PLC recipes via iFA Evolution by converting, modifying, and preparing recipe configurations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[paudyyin](https://clawhub.ai/user/paudyyin)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and automation engineers use this skill to convert iFA .txtrecipe PLC recipe files to CoDeSys text recipes, convert edited recipes back to iFA binary format, and merge cam data from ProdData recipe files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated PLC recipe artifacts may be unsafe or unusable because the conversion scripts have material validation and serialization flaws.

Mitigation: Validate generated recipes independently, especially numeric type widths and RecipeConfig.json schema checksums, before importing or deploying them.

Risk: Using an incorrect or missing RecipeConfig.json can produce recipe files with invalid schema checksum data.

Mitigation: Confirm the RecipeConfig.json path and schema checksum before converting CoDeSys text recipes back to iFA binary recipe files.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/paudyyin/skills/ifa-codesys-recipe)
- [Publisher profile](https://clawhub.ai/user/paudyyin)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with PowerShell command examples and file workflow steps]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires user-provided recipe directories and, for reverse conversion, the correct RecipeConfig.json schema checksum source.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
