## Description:

Google Slides API integration with managed OAuth for inspecting presentations, creating or updating slide content, managing layouts, and coordinating presentation workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hith3sh](https://clawhub.ai/user/hith3sh)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to connect an agent to Google Slides, inspect decks, create and update slide content, manage layouts, and coordinate presentation workflows through ClawLink-managed OAuth.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill depends on the ClawLink plugin and hosted OAuth service for access to Google Slides.

Mitigation: Install only if the user trusts ClawLink with Google Slides account access and reviews Google's requested permissions before connecting.

Risk: Write and destructive actions can change or delete presentation content.

Mitigation: Confirm the target presentation, slide or element and intended effect before creating, updating or deleting content.

Risk: Presentation sharing settings can expose edited content to unintended viewers.

Mitigation: Review presentation sharing permissions before making changes.

## Reference(s):

- [Google Slides Skill Page](https://clawhub.ai/hith3sh/skills/google-slides-presentations)
- [Google Slides API Overview](https://developers.google.com/slides)
- [Google Slides Presentations API Reference](https://developers.google.com/slides/reference/rest/v1/presentations)
- [ClawLink OpenClaw Docs](https://docs.claw-link.dev/openclaw)
- [ClawLink](https://claw-link.dev/?utm_source=clawhub&utm_medium=referral&utm_content=google-slides-presentations)
- [ClawLink Verification](https://claw-link.dev/verify)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include ClawLink tool-call instructions; write or destructive Google Slides changes should be previewed and confirmed before execution.]

## Skill Version(s):

1.0.6 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
