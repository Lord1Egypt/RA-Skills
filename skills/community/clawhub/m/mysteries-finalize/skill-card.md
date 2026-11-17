## Description:

Automates finalization of a Farsight video project by verifying final media assets, generating transcripts and subtitles, localizing subtitle files, producing thumbnail variants, and organizing deliverables.

This skill is ready for commercial/non-commercial use.

## Publisher:

[azizbrownint](https://clawhub.ai/user/azizbrownint)

### License/Terms of Use:

MIT-0

## Use Case:

Content production teams and developers use this skill to prepare final Farsight release assets from a project's Renders/Final/ folder, including transcripts, localized subtitles, and multiple thumbnail formats.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill processes and reorganizes files under a Farsight project's Renders/Final/ folder, so running it in the wrong directory could affect unintended project assets.

Mitigation: Confirm the target project folder and required video, audio, and thumbnail files before executing conversion, translation, thumbnail generation, or cleanup steps.

Risk: Localized subtitle generation uses an external translation library, which may send subtitle text to a third-party translation service depending on configuration.

Mitigation: Review subtitle content and translation provider settings before processing sensitive material.

## Reference(s):


## Skill Output:

**Output Type(s):** [Text, Code, Shell commands, Files, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and Python code; generated TXT, SRT, and image files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Processes local video, audio, and image assets in Renders/Final/ and generates localized subtitles plus thumbnail variants.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
