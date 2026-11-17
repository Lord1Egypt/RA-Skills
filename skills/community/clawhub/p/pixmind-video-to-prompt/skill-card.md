## Description:

Extract a SaaS-style storyboard with local reference frames, timestamps, scripts, scene descriptions, and recreation prompts from one local video or remote URL.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fuyunzhishang](https://clawhub.ai/user/fuyunzhishang)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, creators, and video production teams use this skill to analyze one local video or remote video URL and turn it into a structured storyboard with timestamps, scene descriptions, recreation prompts, and local reference frames.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may download executable Node.js or FFmpeg runtimes from remote, manifest-controlled sources.

Mitigation: Prefer preinstalled Node.js and FFmpeg where possible, and install the skill only when the Pixmind CDN and runtime manifests are trusted.

Risk: Environment-configured endpoints can redirect API credentials and videos.

Mitigation: Avoid custom PIXMIND_API_BASE, PIXMIND_NODE_MANIFEST, or PIXMIND_FFMPEG_MANIFEST values unless the endpoints are controlled and trusted.

Risk: Video analysis uploads video content to the configured Pixmind service.

Mitigation: Do not submit private or sensitive videos unless the user is comfortable uploading them to that service.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/fuyunzhishang/skills/pixmind-video-to-prompt)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration]

**Output Format:** [JSON result with storyboard data, local image attachments, and presentation-ready Markdown table guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes task ID, status, output directory, storyboard fields, screenshot success data, attachments, presentation sections, and raw API response.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
