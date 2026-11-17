## Description:

Monitor Instagram DMs for reels, extract reel or post links from unread conversations, and append sender/link pairs to instagram_reels.csv.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thejas775](https://clawhub.ai/user/thejas775)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to monitor an authenticated Instagram Direct Messages tab for unread messages that contain reels or posts and record the sender ID with the extracted link in a local CSV file.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill inspects an authenticated Instagram Direct Messages tab and can record sender IDs and reel or post links from private conversations.

Mitigation: Run it only on conversations you are comfortable recording, keep the browser tab under user control, and review where instagram_reels.csv will be created before use.

## Reference(s):

- [Instagram Direct Inbox](https://www.instagram.com/direct/inbox/)
- [ClawHub skill page](https://clawhub.ai/thejas775/skills/insta-reel-extractor)
- [Publisher profile](https://clawhub.ai/user/thejas775)

## Skill Output:

**Output Type(s):** [Guidance, Code, Files]

**Output Format:** [Markdown instructions with JavaScript snippets and CSV output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates or appends instagram_reels.csv rows in userid,reel_link format.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
