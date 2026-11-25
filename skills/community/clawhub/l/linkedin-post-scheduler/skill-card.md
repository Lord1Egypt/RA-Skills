## Description:

Schedule, publish, list, edit or cancel LinkedIn posts on the user's own profile with Chime Scheduler. Use when the user asks to post on LinkedIn, schedule a LinkedIn post for a time ("Tuesday at 9", "tomorrow morning"), see what is scheduled, move or change a post, cancel one, delete a post that is already live, or add images or a video.

This skill is ready for commercial/non-commercial use.

## Publisher:

[alihafizji](https://clawhub.ai/user/alihafizji)

### License/Terms of Use:

MIT-0

## Use Case:

Individual LinkedIn account holders use this skill through chat to draft, schedule, publish, review, edit, or cancel posts on their own profile, including posts with images or video.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Publishing immediately is irreversible from the skill.

Mitigation: Show the final post text and ask for confirmation before publishing, unless the user has plainly asked to post it now.

Risk: Cancelling a post that is already live deletes it from LinkedIn and cannot be undone.

Mitigation: Confirm the specific post by its text and publish time before cancelling it.

Risk: A vague or misread local time could schedule a post for the wrong time.

Mitigation: Use the user's local clock, check status when the local date or time zone is needed, and repeat the returned time verbatim after scheduling or editing.

Risk: Retrying a post marked unconfirmed could publish a duplicate.

Mitigation: Ask the user to check their LinkedIn profile and retry only after they confirm the post is absent.

## Reference(s):

- [Chime Scheduler MCP server](https://schedule.getchime.co/mcp)
- [ClawHub skill release](https://clawhub.ai/alihafizji/skills/linkedin-post-scheduler)

## Skill Output:

**Output Type(s):** [Text, Markdown]

**Output Format:** [Plain-language summaries and Markdown tables]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Status summaries, scheduled times, post text, and media confirmation details when available]

## Skill Version(s):

1.1.0 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
