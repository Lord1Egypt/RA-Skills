## Description:

Interactively helps an agent collect an Instagram username, download directory, cookie file path, and optional proxy, then prepare a gallery-dl command for downloading posts, Reels, avatars, or individual posts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zitao666](https://clawhub.ai/user/zitao666)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to guide Instagram media downloads by collecting required parameters and preparing the corresponding gallery-dl command. It is intended for local use with a user-provided Instagram cookie file and optional proxy.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks the agent to use an Instagram cookie file locally, which can expose session credentials if the cookie contents are pasted into chat or shared.

Mitigation: Keep the cookie file private, do not paste sessionid, csrftoken, or cookie contents into chat, and delete the cookie file when the download task is complete.

Risk: The generated shell command is built from user-provided username, proxy, and file path values.

Mitigation: Validate the Instagram username, proxy URL, and local file paths before running the command, and execute only after confirming the exact command with the user.

Risk: The artifact mentions using --no-check-certificate for proxy certificate issues, which can weaken TLS verification.

Mitigation: Avoid --no-check-certificate unless the user explicitly accepts the security tradeoff after reviewing the proxy configuration.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zitao666/skills/instagram-downloader)
- [Publisher profile](https://clawhub.ai/user/zitao666)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include local file paths, an optional proxy value, and a user-provided cookie file path.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
