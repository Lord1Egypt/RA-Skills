## Description:

Mood Checkin helps users run short emotional check-ins, guided breathing, journaling, venting, weekly recaps, and shareable mood summaries through the Sol persona.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sharoonsharif](https://clawhub.ai/user/sharoonsharif)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill for private self-reflection through mood check-ins, breathing and grounding guidance, journaling prompts, venting support, and periodic mood recaps. It is positioned as a friendly check-in companion rather than therapy or medical care.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores sensitive emotional check-ins and derived patterns in a local mood-checkin-profile.json file.

Mitigation: Use the skill in a private workspace, avoid committing or syncing the profile file, and review or delete the file when the stored history is no longer needed.

Risk: Shareable weather reports, archetypes, and monthly wrapped summaries can expose sensitive personal information.

Mitigation: Inspect, redact, or avoid sharing generated summaries when they reveal private emotional patterns or circumstances.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sharoonsharif/skills/mood-checkin)
- [International Association for Suicide Prevention crisis centres](https://www.iasp.info/resources/Crisis_Centres/)

## Skill Output:

**Output Type(s):** [Text, Markdown, Files, Guidance]

**Output Format:** [Conversational text and Markdown-style shareable cards, with a local JSON mood profile file]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May read and update mood-checkin-profile.json in the current working directory.]

## Skill Version(s):

2.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
