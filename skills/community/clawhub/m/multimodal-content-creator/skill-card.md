## Description:

End-to-end multimodal content creation workflow for receiving WhatsApp text or voice requests, transcribing audio with Whisper, generating images with DALL-E 3, and replying automatically.

This skill is ready for commercial/non-commercial use.

## Publisher:

[terrycarter1985](https://clawhub.ai/user/terrycarter1985)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and creators use this skill to automate a WhatsApp-driven content workflow that turns customer text or voice requests into image-generation prompts, generated image files, and automated replies.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles WhatsApp authentication tokens with limited containment.

Mitigation: Review token storage before installation, run in an isolated environment, and avoid production credentials until token handling is hardened.

Risk: The workflow processes local media paths and customer content.

Mitigation: Validate media paths and avoid real customer data until local file handling has been reviewed.

Risk: The workflow can send automated replies based on generated or transcribed content.

Mitigation: Add a human confirmation or approval step before sending replies to customers.

Risk: Dependencies are specified with lower bounds rather than pinned versions.

Mitigation: Pin and review dependencies before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/terrycarter1985/skills/multimodal-content-creator)

## Skill Output:

**Output Type(s):** [Text, Files, Shell commands, Configuration]

**Output Format:** [Markdown instructions, CLI output, transcription text, WhatsApp reply text, and generated PNG image files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires OpenAI API credentials and WhatsApp CLI authentication; generated files are written locally.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
