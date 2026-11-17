## Description:

Publish, edit, or configure notes on Mowen via its Open API, including social-media-style notes with rich text and images.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jacobluo](https://clawhub.ai/user/jacobluo)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to create, edit, and configure Mowen notes through the Mowen Open API, including rich text, tags, images, drafts, and publishing settings.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Note content and selected images are sent to Mowen during publishing and upload workflows.

Mitigation: Use the skill only for content intended for Mowen, review note text and image paths before execution, and keep the API key in MOWEN_API_KEY rather than passing it on the command line.

Risk: The documented privacyType setting is not applied during note creation.

Mitigation: Confirm whether the created note is public or draft before publishing, and use the settings action to apply privacy controls until creation either applies privacyType or rejects it explicitly.

Risk: Local image uploads use a server-provided upload destination.

Mitigation: Upload only intended local image files and review the skill before deployment if upload destination validation is required for the environment.

## Reference(s):

- [Mowen Open API Reference](references/mowen_api.md)
- [ClawHub Skill Page](https://clawhub.ai/jacobluo/skills/mowenskill)
- [ClawHub Publisher Profile](https://clawhub.ai/user/jacobluo)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration]

**Output Format:** [Markdown guidance with JSON examples, shell commands, and JSON command results from the publishing script]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires MOWEN_API_KEY for authenticated Mowen API operations; the publish script can read note JSON from a file or stdin.]

## Skill Version(s):

1.0.3 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
