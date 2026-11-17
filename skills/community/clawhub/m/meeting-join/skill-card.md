## Description:

智能会议机器人 helps agents join online meetings through platform APIs, manage meeting lifecycle and voice state, transcribe discussions, generate summaries and action items, and handle TTS events.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

Employees, teams, and workflow builders use this skill to automate meeting participation, transcription, summaries, and follow-up tasks for online meetings that provide platform APIs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may join, listen to, transcribe, attribute speakers in, and save records from meetings that contain sensitive or identifiable information.

Mitigation: Require explicit per-meeting approval, participant notice or consent, defined storage, and retention and deletion rules before use.

Risk: The artifact declares exec capability without enforceable command constraints in the provided evidence.

Mitigation: Avoid granting exec unless the publisher provides narrow command constraints and the deployment enforces a limited command and file-access policy.

Risk: Meeting transcriptions and speaker attribution can be inaccurate when audio quality is poor, accents vary, or participants speak over one another.

Mitigation: Review generated transcripts, summaries, and action items before treating them as final meeting records.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/meeting-join)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown and text with inline shell commands and structured meeting records]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include meeting status events, transcripts, summaries, action items, TTS event notes, and setup guidance.]

## Skill Version(s):

1.0.1 (source: server release metadata and target metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
