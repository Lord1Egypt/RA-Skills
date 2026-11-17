## Description:

Organize a photo folder by cleaning non-photo files, removing bad exposures, detecting blur and burst shots, and classifying photos into numbered subfolders using AI vision analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lemondepat](https://clawhub.ai/user/lemondepat)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to organize a single photo folder by separating non-photo files, identifying low-quality images, grouping burst shots, and sorting remaining photos into numbered categories. It is suited for guided cleanup workflows where the user reviews proposed file moves or deletions before they are applied.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automatic installation of unpinned Python packages can introduce unexpected dependency changes.

Mitigation: Use an isolated virtual environment with pinned dependencies and avoid the automatic pip-install snippets.

Risk: Predictable /tmp analysis files can influence later file move or deletion steps.

Mitigation: Review generated analysis files and verify the exact photo paths before approving cleanup actions.

Risk: Photo cleanup can permanently delete user files if deletion options are approved incorrectly.

Mitigation: Prefer moving rejected photos into review folders over permanent deletion.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, JSON]

**Output Format:** [Markdown guidance with shell commands, Python snippets, summary tables, and JSON analysis artifacts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose local file moves or deletions after user confirmation; Python analysis writes /tmp/photo_analysis.json.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
