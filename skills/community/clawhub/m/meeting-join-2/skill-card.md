## Description:

Helps an agent join supported online meetings, track meeting and voice state, provide TTS responses, transcribe discussion, and generate summaries and action items.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and teams use this skill to configure an agent-assisted meeting bot for supported meeting platforms, including joining meetings, tracking speaker state, transcribing discussion, and creating post-meeting summaries and tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can be used to join, listen to, transcribe, and save meetings without clearly defined consent controls.

Mitigation: Require explicit organizer and participant consent before the bot joins or records any meeting, and confirm that the behavior complies with the meeting platform policy.

Risk: Meeting transcripts, summaries, and action items may contain sensitive information without defined retention, access, or deletion rules.

Mitigation: Define where meeting records are stored, who can access them, how long they are retained, and how they are deleted before deployment.

Risk: The artifact requests read, write, and exec authority plus generic API and callback configuration.

Mitigation: Manually review API credentials, callback URLs, and command execution paths, and run the skill with the minimum permissions needed for the approved meeting workflow.

Risk: Transcription and speaker attribution can be inaccurate, especially with noise, accents, or overlapping speech.

Mitigation: Label generated transcripts and summaries as machine-produced and require human review before using them as official records or task assignments.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/meeting-join-2)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with configuration tables, examples, and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include meeting summaries, transcripts, action items, status events, and API credential setup guidance.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
