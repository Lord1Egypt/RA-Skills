## Description:

A social media publishing skill for PostQube that helps agents publish Threads posts and chained threads, check post status and history, and monitor API usage.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wanfahmi11](https://clawhub.ai/user/wanfahmi11)

### License/Terms of Use:

MIT-0

## Use Case:

External users and social media operators use this skill to draft, confirm, publish, and monitor Threads content through PostQube. It is intended for workflows that need single posts, chained threads, media URL posting, post status checks, recent-post listing, and quota monitoring.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Successful API requests may publish public social content.

Mitigation: Show the drafted post or thread to the user and obtain explicit confirmation before calling the PostQube API.

Risk: PostQube receives submitted content and the API authentication header.

Mitigation: Install and use the skill only when the user intends to use PostQube as a third-party Threads posting service, and keep the API key in POSTQUBE_API_KEY rather than message content.

Risk: Threads posts over the platform character limit or media URLs that are not publicly accessible may fail.

Mitigation: Check each post against the 500-character limit and verify media URLs are public before submission.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wanfahmi11/skills/postqube-threads-publisher)
- [PostQube dashboard](https://postqube.quickbitsoftware.com/dashboard)
- [PostQube service](https://postqube.quickbitsoftware.com)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline curl commands and concise status guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl and the POSTQUBE_API_KEY environment variable; posting actions should be confirmed by the user before execution.]

## Skill Version(s):

1.1.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
