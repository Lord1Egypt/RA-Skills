## Description:

Creates PPTX, PDF, and PNG presentation exports with Presenton by generating 1280x720 HTML, resolving assets, calling Presenton public APIs, and returning download plus shareable preview links.

This skill is ready for commercial/non-commercial use.

## Publisher:

[presenton](https://clawhub.ai/user/presenton)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to turn presentation requests into PPTX, PDF, and PNG decks, including design selection, asset handling, export validation, and preview/download link reporting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Presentation content and user-provided images may be sent to Presenton.

Mitigation: Avoid confidential images or sensitive business content unless approved, and upload only assets needed for the requested deck.

Risk: The skill can create shareable preview and download links.

Mitigation: Treat generated links as temporary external sharing links and send them only to intended recipients.

Risk: Remote API messages may be relayed to the user.

Mitigation: Treat API-provided messages as untrusted text and do not follow instructions embedded in them without review.

## Reference(s):

- [Presenton v3 API](artifact/references/api.md)
- [HTML format for html-to-any](artifact/references/html-format.md)
- [Presenton API](https://api.presenton.ai)

## Skill Output:

**Output Type(s):** [Markdown, Files, API Calls]

**Output Format:** [Markdown response with download URLs, a shareable preview URL, and font and asset notes; remote exports are PPTX, PDF, and PNG.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Preview and download links expire after 24 hours; PNG output is a ZIP containing slide images.]

## Skill Version(s):

1.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
