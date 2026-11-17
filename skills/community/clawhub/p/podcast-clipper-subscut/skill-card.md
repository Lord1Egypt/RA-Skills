## Description:

Podcast Clipper turns long podcasts, interviews, webinars, and talking-head videos into short clips for TikTok, Reels, or YouTube Shorts through Subscut's API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[arpittiwari24](https://clawhub.ai/user/arpittiwari24)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, marketers, and agent users use this skill to repurpose long-form spoken videos into captioned short-form clips with titles, scores, clip URLs, and timestamps.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can send the Subscut API key to a configured HTTPS API endpoint.

Mitigation: Keep SUBSCUT_API_BASE_URL at the default https://subscut.com unless deliberately testing with a separate non-production key, and rotate the key if it may have been used with an untrusted endpoint.

Risk: The skill sends the provided video URL and processing request to Subscut.

Mitigation: Install and use the skill only when sharing the source video URL and related clipping request with Subscut is acceptable.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/arpittiwari24/skills/podcast-clipper-subscut)
- [Subscut agent documentation](https://subscut.com/agents)
- [Subscut API base URL](https://subscut.com)

## Skill Output:

**Output Type(s):** [JSON, Shell commands, Configuration, Guidance]

**Output Format:** [JSON response with clip URLs, titles, scores, and timestamps; Markdown or shell commands when explaining usage.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires npm and a SUBSCUT_API_KEY; supports optional SUBSCUT_API_BASE_URL, clip count, caption style, render format, captions, and duration bounds.]

## Skill Version(s):

1.0.3 (source: server release metadata; artifact metadata reports 1.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
