## Description:

Netease Music Pusher helps an agent fetch NetEase Cloud Music personalized daily recommendations and public chart song lists, with login, cookie reuse, formatted song details, and scheduling guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[t-evan](https://clawhub.ai/user/t-evan)

### License/Terms of Use:

MIT

## Use Case:

Agent operators use this skill to retrieve and format NetEase Cloud Music daily recommendations or public chart tracks for scheduled music updates. It is suited for personal or workspace automations that can handle account login state and service-specific network access.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Reusable NetEase login cookies are persisted in secrets/netease_cookies.json and should be treated as password-equivalent session material.

Mitigation: Use the skill only in a private workspace, restrict access to the secrets directory, and delete the cookie file when it is no longer needed.

Risk: Phone numbers and SMS verification codes may be entered as shell arguments, where they can be exposed through shell history or process logging.

Mitigation: Avoid placing real phone numbers or SMS codes directly in persistent shell commands, saved scripts, shared logs, or automation records.

## Reference(s):

- [Netease Music Pusher on ClawHub](https://clawhub.ai/t-evan/skills/netease-music-pusher)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown-style text with shell command snippets and formatted song-list output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include song titles, artists, albums, recommendation reasons, NetEase song links, login status messages, and cron configuration examples.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
