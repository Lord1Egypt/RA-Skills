## Description:

Provides a concise Chinese daily brief with Nantong weather and the top five V2EX hot topics when requested or on a scheduled morning run.

This skill is ready for commercial/non-commercial use.

## Publisher:

[muzhang111](https://clawhub.ai/user/muzhang111)

### License/Terms of Use:

MIT-0

## Use Case:

Chinese-speaking users use this skill to receive a short morning briefing for Nantong weather and current V2EX discussion topics. It is suited for user-triggered briefings or a deliberately configured 8:00 AM scheduled run.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A broad or frequent scheduled trigger could interrupt normal conversations with an unsolicited daily brief.

Mitigation: Configure scheduling deliberately for the intended 8:00 AM run and keep trigger phrases specific to briefings.

Risk: The brief depends on public weather and V2EX endpoints, so unavailable or changed responses can produce missing or incomplete content.

Mitigation: Handle request failures by telling the user to retry later, as described in the artifact notes.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/muzhang111/skills/muzhang111-daily-brief)
- [Publisher profile](https://clawhub.ai/user/muzhang111)
- [wttr.in Nantong weather endpoint](https://wttr.in/Nantong?format=3)
- [V2EX hot topics API](https://www.v2ex.com/api/topics/hot.json)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown-style daily brief with weather text and a numbered list of V2EX topics]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Chinese-language brief; normally limited to Nantong weather and five V2EX hot topics.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
