## Description: <br>
Google Slides API integration with managed OAuth. Inspect presentations, create or update slide content, manage layouts, and coordinate presentation workflows. Use this skill when users want to work with Google Slides decks programmatically. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hith3sh](https://clawhub.ai/user/hith3sh) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to inspect Google Slides presentations, create or update slides and presentation elements, and manage deck workflows through a connected Google account. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release evidence reports a suspicious security verdict tied to an autoreview helper that can run with sandbox-bypass authority. <br>
Mitigation: Install only in trusted ClawHub-maintenance workflows, prefer --no-yolo or AUTOREVIEW_YOLO=0 for autoreview, and review commands that can post to GitHub, change moderation state, or send diffs to external reviewer CLIs. <br>
Risk: The skill uses OAuth-backed access to a user's Google Slides data and can perform write operations. <br>
Mitigation: Use the connected account intentionally, verify the target presentation and requested change, preview write operations when available, and require explicit user confirmation before create, update, or delete actions. <br>


## Reference(s): <br>
- [Google Slides API Overview](https://developers.google.com/slides) <br>
- [Google Slides Presentations Reference](https://developers.google.com/slides/reference/rest/v1/presentations) <br>
- [ClawLink OpenClaw Docs](https://docs.claw-link.dev/openclaw) <br>
- [ClawLink Verification](https://claw-link.dev/verify) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and tool-call examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces guidance for authenticated Google Slides API operations through ClawLink-managed tools.] <br>

## Skill Version(s): <br>
1.0.6 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
