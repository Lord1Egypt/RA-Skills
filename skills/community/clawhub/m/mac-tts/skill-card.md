## Description:

Provides text-to-speech on macOS using the built-in `say` command for voice notifications, audio alerts, reading text aloud, and announcements through Mac speakers, with examples for Chinese, English, and Japanese voices.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kalijason](https://clawhub.ai/user/kalijason)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill on macOS to speak notifications, alerts, reminders, warnings, or supplied text aloud through the system speakers.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can cause audible output through Mac speakers, which may be inappropriate in quiet, shared, or sensitive environments.

Mitigation: Use it only where spoken output is expected and acceptable.

Risk: The examples include checking, unmuting, and changing system volume before speech.

Mitigation: Review volume-related commands before use and avoid them when changing system audio settings would be disruptive.

## Reference(s):


## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown guidance with inline shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Targets macOS local audio output; speech runs synchronously unless the command is run asynchronously.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
