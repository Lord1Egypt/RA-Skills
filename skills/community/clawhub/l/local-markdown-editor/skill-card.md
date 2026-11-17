## Description:

Local Markdown Editor with Live Preview is a web-based Markdown editor that opens a local Flask server and provides real-time editing with live preview, synchronized scrolling, and toolbar controls for Markdown tags.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xiyunnet](https://clawhub.ai/user/xiyunnet)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, technical writers, and local users use this skill to launch a localhost Markdown editor for editing Markdown files with a live preview and direct save workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The local web server exposes broad file access and save behavior with weak boundaries.

Mitigation: Run only on trusted local files in a private environment, and constrain reads and writes to an approved workspace and Markdown-like extensions before broader use.

Risk: Global CORS and unauthenticated local routes may allow unintended local interactions if exposed beyond localhost or triggered by crafted URLs.

Mitigation: Keep the server bound to localhost, avoid opening untrusted editor URLs, and add a startup token or comparable local authentication before deployment.

Risk: Automatic shutdown on page hide or unload can interrupt editing sessions or be triggered unexpectedly.

Mitigation: Prefer explicit shutdown controls or confirm shutdown behavior in the target environment before relying on the editor for important files.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xiyunnet/skills/local-markdown-editor)
- [Markdown Guide](https://www.markdownguide.org/)
- [Flask Documentation](https://flask.palletsprojects.com/)
- [Showdown.js](https://github.com/showdownjs/showdown)
- [CodeMirror](https://codemirror.net/)

## Skill Output:

**Output Type(s):** [Markdown, Code, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with inline shell commands and local web editor output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local file edits through a browser-based Markdown editor backed by a localhost Flask server.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
