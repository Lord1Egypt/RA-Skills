## Description:

Generates Chinese interior design proposal PowerPoint decks for commercial or residential projects from project details and optional render images.

This skill is ready for commercial/non-commercial use.

## Publisher:

[137984917-cyber](https://clawhub.ai/user/137984917-cyber)

### License/Terms of Use:

MIT-0

## Use Case:

Interior designers and proposal teams use this skill to create client-facing PPT proposal decks for commercial spaces or residential projects. It supports project type, name, area, style, budget, spaces, company, designer, and optional local images.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Dependency installation may affect a shared Python environment.

Mitigation: Install python-pptx and Pillow in a virtual environment and consider pinning package versions.

Risk: The generated proposal may not match the user's project context or design requirements.

Mitigation: Use the skill only for Chinese interior-design proposal decks based on provided project details, then review the PPT before client delivery.

Risk: Optional local images may be unsuitable or unintended for inclusion.

Mitigation: Provide only approved local render images and inspect the generated image slides before sharing.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/137984917-cyber/skills/interior-proposal)
- [Design Document Template](references/design-doc.md)
- [PPT Outline Template](references/ppt-outline.md)

## Skill Output:

**Output Type(s):** [files, shell commands, guidance]

**Output Format:** [PowerPoint presentation file plus console status messages and usage guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces 12-14 slide .pptx proposal decks; optional local images can be inserted into rendering pages.]

## Skill Version(s):

4.1.0 (source: server release metadata and artifact skill.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
