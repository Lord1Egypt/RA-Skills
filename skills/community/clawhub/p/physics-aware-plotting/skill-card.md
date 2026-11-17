## Description:

Physics-aware scientific plotting for research repositories. Use before making or updating Matplotlib figures to identify axis meanings, the comparison the figure supports, physically meaningful axis ranges, appropriate linear/log scaling, and publication-style visual choices inspired by ApJ/AAS figures.

This skill is ready for commercial/non-commercial use.

## Publisher:

[soyonaoc](https://clawhub.ai/user/soyonaoc)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and researchers use this skill when creating or revising scientific figures so an agent considers physical quantities, comparison goals, axis ranges, scaling, and publication-quality plotting conventions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may lead an agent to create or move plotting outputs in repository directories.

Mitigation: Review repository file changes before accepting generated figures, tables, or slide assets.

Risk: Poorly chosen axis limits, scales, labels, or legends could make scientific plots misleading.

Mitigation: Check the physical quantity on each axis, the intended comparison, meaningful nonzero ranges, and labels before using figures in papers or slides.

## Reference(s):


## Skill Output:

**Output Type(s):** [Guidance, Code, Shell commands, Configuration, Files]

**Output Format:** [Markdown guidance with code, shell commands, or file changes when plotting work requires them]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May result in generated or moved plotting assets under outputs/, data_save/, or slides/assets/.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
