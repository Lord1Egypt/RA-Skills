## Description:

Prepare a user for an upcoming meeting or event by listing next-day calendar events, prompting for a selection, researching the topic and participants, producing an executive summary, and generating a fully produced 3-5 minute audio briefing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sourishkrout](https://clawhub.ai/user/sourishkrout)

### License/Terms of Use:

MIT-0

## Use Case:

Employees and external-facing teams use this skill to prepare for high-stakes meetings by selecting a next-day calendar event, researching the topic and public participant context, and receiving a concise written prep package plus a 3-5 minute audio briefing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow may expose next-day calendar details and selected meeting context to Contextual.ai and an audio provider such as ElevenLabs or Chatterbox.

Mitigation: Use it only for meetings approved for those third-party data flows, and avoid confidential meetings unless the user has approval.

Risk: Meeting research may include weak or stale public information about topics or participants.

Mitigation: Apply the source credibility rubric, cite attributable sources, distinguish facts from inferences, and lower confidence when evidence is weak.

Risk: Generated prep guidance could create overconfident or misleading meeting recommendations.

Mitigation: Keep the briefing concise, include explicit risks and unknowns, and require user review before acting on recommendations.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/sourishkrout/skills/imposter-smasher)
- [Workflow Rubric](references/workflow-rubric.md)
- [Source Credibility Rubric](references/source-credibility-rubric.md)
- [Executive Summary Template](references/executive-summary-template.md)
- [Audio Brief Template](references/audio-brief-template.md)
- [Implementation Notes](references/implementation-notes.md)

## Skill Output:

**Output Type(s):** [text, markdown, audio, shell commands, configuration, guidance]

**Output Format:** [Markdown executive summary, plain-text audio script, JSON audio manifest, and MP3 or WAV audio artifact paths or links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Targets a 180-300 second spoken briefing and labels confidence for uncertain claims.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
