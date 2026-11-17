## Description:

Generate daily Chinese classical poetry art cards with AI-generated landscape images paired with poem text and delivered to chat.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lava-lake](https://clawhub.ai/user/lava-lake)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to create a daily Chinese classical poetry image card, combine it with the poem text, and deliver the result through chat or a scheduled automation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Poem titles or memory-derived text may be sent to an external MiniMax-backed image service.

Mitigation: Review the text included in image prompts and use the skill only when external processing by the configured MiniMax service is acceptable.

Risk: Generated content can be posted automatically to Telegram or another chat destination.

Mitigation: Configure the cron schedule and chat destination explicitly, and review automated delivery settings before enabling recurring runs.

Risk: The image workflow writes to a local output directory and depends on an external CLI installation.

Mitigation: Use an isolated output directory and prefer a pinned or local MiniMax CLI installation before running the script.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lava-lake/skills/poetry-daily-art)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration instructions, Files]

**Output Format:** [Generated image file path plus formatted chat caption]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the mmx CLI, a MiniMax API key, poem progress data, and an explicitly configured chat delivery destination.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
