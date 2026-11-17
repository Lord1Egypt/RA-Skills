## Description:

Meixin Meeting Assistant generates structured internal Meixin Healthcare meeting minutes from meeting audio by transcribing with Fun-ASR, standardizing healthcare and insurance terminology, attributing speakers, and archiving outputs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jiadong0723](https://clawhub.ai/user/jiadong0723)

### License/Terms of Use:

MIT-0

## Use Case:

Employees and internal operations teams use this skill to turn Chinese meeting recordings into standardized healthcare and insurance meeting minutes with speaker attribution, terminology normalization, action items, and archived raw transcripts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles sensitive meeting recordings and transcripts.

Mitigation: Require explicit participant consent, documented retention rules, and approved storage before use.

Risk: The evidence reports an embedded DashScope API key.

Mitigation: Remove the embedded credential, rotate the key, and require runtime secret injection through DASHSCOPE_API_KEY.

Risk: The workflow depends on publicly reachable audio URLs.

Mitigation: Use approved private storage or short-lived signed URLs instead of public CDN handling.

Risk: The skill requests broad access to historical meeting memory.

Mitigation: Limit memory access to user-approved records needed for the current meeting.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jiadong0723/skills/jiadong-meixin-meeting)
- [DashScope transcription API endpoint](https://dashscope.aliyuncs.com/api/v1/services/audio/asr/transcription)

## Skill Output:

**Output Type(s):** [Text, Markdown, Files, Shell commands, Configuration]

**Output Format:** [Markdown meeting minutes and plain-text raw transcripts, with supporting command or configuration guidance when needed]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are intended for persistent meeting-memory storage and may include speaker labels, normalized terminology, consensus items, and TODOs.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
