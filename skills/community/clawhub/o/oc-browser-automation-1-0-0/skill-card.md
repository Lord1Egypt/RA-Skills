## Description:

Browser control helper that wraps OpenClaw browser operations for web automation, screenshots, clicking, typing, scrolling, tab management, uploads, downloads, and page snapshots.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vlvwlw](https://clawhub.ai/user/vlvwlw)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to drive browser workflows such as opening pages, collecting screenshots or snapshots, interacting with page elements, uploading and downloading files, and debugging page behavior.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can act through browser sessions, including sessions that may already be logged in.

Mitigation: Use it deliberately, avoid connecting it to a personal Chrome profile unless needed, and review browser actions before using authenticated sessions.

Risk: Screenshots and snapshots may expose sensitive data from logged-in pages.

Mitigation: Check screenshots and snapshots for sensitive data before sharing or storing them outside the session.

Risk: The skill supports file uploads and downloads.

Mitigation: Confirm upload sources, download destinations, and file contents before transferring files through browser workflows.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/vlvwlw/skills/oc-browser-automation-1-0-0)
- [Publisher profile](https://clawhub.ai/user/vlvwlw)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline browser command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May reference browser snapshots, page screenshots, tabs, downloads, uploads, console output, network requests, trace recordings, and element refs.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
