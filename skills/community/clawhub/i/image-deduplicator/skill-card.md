## Description:

Detect and remove exact or similar duplicate images in folders using perceptual and MD5 hashing with configurable similarity and actions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mingo-318](https://clawhub.ai/user/mingo-318)

### License/Terms of Use:


## Use Case:

Developers, data practitioners, and image dataset maintainers use this skill to scan local folders for exact or near-duplicate images and decide whether to list, move, or delete duplicate files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Duplicate cleanup can remove or relocate files the user intended to keep.

Mitigation: Run the listing mode first, review duplicate groups, and keep backups before using delete or move actions.

Risk: Near-duplicate detection may group visually similar images that are not true duplicates.

Mitigation: Use a conservative threshold and review reported groups before taking destructive action.

Risk: Dependency versions can affect image hashing behavior and reproducibility.

Mitigation: Install dependencies in a virtual environment and pin versions when repeatable results matter.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, shell commands, code, guidance]

**Output Format:** [Markdown guidance with CLI commands and terminal output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports duplicate image groups and may move or delete duplicate files when the user explicitly selects those actions.]

## Skill Version(s):

1.0.0 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
