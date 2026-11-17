## Description:

Use when the user wants to download a public video or GIF from X (Twitter), or a public video from TikTok, Vimeo, or Facebook. Trigger when they say "download this tweet", "save this X video", "grab this GIF", or paste an x.com, twitter.com, TikTok, Vimeo, or Facebook video URL. Do not use it for YouTube, Instagram, or Bilibili.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xuxizhen](https://clawhub.ai/user/xuxizhen)

### License/Terms of Use:

MIT-0

## Use Case:

External users can provide a public video link to retrieve media from X, TikTok, Vimeo, or Facebook, including animated GIFs from X. The skill reports the resulting file and where it was saved.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Video URLs may contain tracking or other sensitive query parameters, and submitted links are shared with the GrabGrab service.

Mitigation: Use only public links you are comfortable sharing with GrabGrab, and remove unnecessary tracking or sensitive query parameters before submitting them.

Risk: The service's live behavior has not been independently verified, and the optional CLI is not included in this release package.

Mitigation: Use the documented service methods, review the service before sending links, and do not rely on the optional CLI being available in this package.

## Reference(s):

- [GrabGrab](https://www.grabgrab.fun)
- [GrabGrab developer documentation](https://www.grabgrab.fun/en/developers)
- [GrabGrab assistant notes](https://www.grabgrab.fun/llms.txt)
- [GrabGrab MCP endpoint](https://www.grabgrab.fun/api/mcp)

## Skill Output:

**Output Type(s):** [API calls, Shell commands, Files, Guidance]

**Output Format:** [JSON service responses, downloaded video files, and concise Markdown or plain-text status reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Downloaded media depends on the selected public link and available quality; private or deleted posts cannot be retrieved.]

## Skill Version(s):

1.2.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
