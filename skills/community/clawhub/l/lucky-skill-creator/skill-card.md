## Description:

Create or update AgentSkills for designing, structuring, validating, and packaging skills with scripts, references, and assets.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rmbell09-lang](https://clawhub.ai/user/rmbell09-lang)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to create, refine, validate, and package agent skills with structured instructions and optional bundled resources.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated or edited skill content could contain incomplete, inaccurate, or unsafe instructions.

Mitigation: Review the generated SKILL.md and bundled resources, then validate and scan the skill before packaging or sharing it.

Risk: Bundled scripts can create or edit files in directories selected by the user.

Mitigation: Run the skill in a scoped workspace and avoid targeting broad home, system, or sensitive directories.

Risk: Packaging may include unintended files from the selected skill directory.

Mitigation: Inspect the skill directory before packaging and keep only files required for the released skill.

## Reference(s):


## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration, Files]

**Output Format:** [Markdown with inline code blocks and file-oriented instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or modify skill files and package .skill archives in directories chosen by the user.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
