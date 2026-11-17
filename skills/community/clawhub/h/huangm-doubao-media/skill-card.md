## Description:

Doubao Media helps agents use an authenticated Doubao web session to test chat completion flows, extract media URLs from SSE responses, and capture or download generated image and video assets from browser network traffic.

This skill is ready for commercial/non-commercial use.

## Publisher:

[huangm199](https://clawhub.ai/user/huangm199)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to operate a Doubao web session, verify chat access, capture generated media URLs, and save image or video assets for follow-on analysis or archiving.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles authenticated browser cookies and stores session data in plaintext.

Mitigation: Use a dedicated browser profile for Doubao, inspect or delete the session file after use, and avoid sharing the profile with unrelated services.

Risk: Network capture can include unrelated ByteDance, Douyin, or mixed browsing traffic.

Mitigation: Run capture only in a controlled session with unrelated tabs and logins closed, and review generated manifests before retaining or sharing them.

Risk: Captured media URLs and downloaded files may include sensitive generated content.

Mitigation: Store captures in a controlled output directory, review contents before distribution, and delete files that are no longer needed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/huangm199/skills/huangm-doubao-media)
- [Doubao web app](https://www.doubao.com/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance, JSON, files]

**Output Format:** [Markdown guidance with inline shell commands; helper scripts emit JSON, JSONL, text summaries, and downloaded media files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires an authenticated Doubao browser session and access to a browser remote debugging port.]

## Skill Version(s):

1.0.1 (source: server release evidence and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
