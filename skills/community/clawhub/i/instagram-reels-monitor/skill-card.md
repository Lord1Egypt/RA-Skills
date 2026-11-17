## Description:

Monitor Instagram DMs for reels by checking unread messages, extracting reel links, and appending sender IDs with reel URLs to a local CSV file.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thejas775](https://clawhub.ai/user/thejas775)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agent operators use this skill to inspect an already authenticated Instagram Direct Messages tab for unread reel messages and record sender IDs plus reel links in a local CSV.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The agent inspects an authenticated Instagram DM tab and can see message and sender information during the workflow.

Mitigation: Use the skill only with an Instagram session and DM tab you intentionally provide for this task.

Risk: The skill saves sender IDs and reel links to a local instagram_reels.csv file.

Mitigation: Review, protect, or delete instagram_reels.csv when the saved data is no longer needed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thejas775/skills/instagram-reels-monitor)
- [Instagram Direct inbox](https://www.instagram.com/direct/inbox/)

## Skill Output:

**Output Type(s):** [text, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JavaScript snippets and CSV output expectations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates or appends local CSV rows in the format userid,reel_link.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
