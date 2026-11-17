## Description:

Refined DaVinci API workflow: images are now imported strictly into a Media Pool bin first, and timeline injection requires explicit user confirmation to prevent errors in complex projects.

This skill is ready for commercial/non-commercial use.

## Publisher:

[azizbrownint](https://clawhub.ai/user/azizbrownint)

### License/Terms of Use:

MIT-0

## Use Case:

External creators and video-production agents use this skill to prepare Farsight Mysteries media projects by transcribing audio, generating timestamped 1080p JPG images, and importing them into DaVinci Resolve with an explicit confirmation gate before timeline injection.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill includes safety-filter bypass guidance for image prompts.

Mitigation: Remove or revise bypass language before installation and require generated prompts to comply with the active image-generation policy.

Risk: The workflow can create local files and modify an open DaVinci Resolve project.

Mitigation: Keep explicit user confirmation before filesystem changes and before timeline injection, and verify the target project, media folder, and timeline before running scripts.

Risk: The artifact includes a backup skill file that may not reflect current release guidance.

Mitigation: Use SKILL.md as the current release artifact and do not rely on SKILL.md.bak for operational instructions.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown workflow guidance with inline shell commands, DaVinci Resolve API scripting notes, and user-confirmation prompts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces instructions for local transcription, image generation, JPG file handling, Media Pool import, and optional timeline placement after explicit user approval.]

## Skill Version(s):

1.1.2 (source: server release evidence, clawhub.json, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
