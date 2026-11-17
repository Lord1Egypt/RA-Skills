## Description:

AI sales coach that sends personalized morning briefings, tracks rep patterns over time, and uses MeetMatch's ML predictions to make your agent smarter about sales outcomes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[brettonb](https://clawhub.ai/user/brettonb)

### License/Terms of Use:

MIT-0

## Use Case:

Sales reps and sales managers use this skill through an OpenClaw agent to receive personalized morning briefings, meeting prep, no-show risk context, performance snapshots, and coaching nudges based on MeetMatch data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can email sensitive employee and prospect performance briefings automatically.

Mitigation: Confirm approved recipients, delivery rules, and access controls before enabling scheduled briefings.

Risk: Persistent coaching memory may retain transcript-derived observations about reps and prospects.

Mitigation: Define notice, consent, retention, and deletion practices with sales, HR, legal, and security stakeholders before installation.

Risk: Broad keyword and schedule triggers may activate coaching workflows more often than intended.

Mitigation: Narrow or disable automatic triggers where possible and require explicit user requests for sensitive briefings.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/brettonb/skills/meetmatch-sales-coach)
- [MeetMatch](https://www.meetmatch.ai)
- [OpenClaw Integration Guide](https://www.meetmatch.ai/integrations/openclaw)
- [MeetMatch OpenClaw API](https://www.meetmatch.ai/api/openclaw)
- [Interactive Demo](https://www.meetmatch.ai/demo/clawcon)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Conversational text and Markdown-style sales briefings]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires MeetMatch API credentials, organization ID, briefing hour, and delivery method configuration.]

## Skill Version(s):

1.0.0 (source: server release evidence and artifact/skill.yaml)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
