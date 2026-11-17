## Description:

Real-time voice streaming via MiniMax WebSocket API for low-latency voice conversations and streaming audio generation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ogdegenblaze](https://clawhub.ai/user/ogdegenblaze)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to test a MiniMax text-to-audio connection and generate speech audio from supplied text using a MiniMax API key.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Security evidence reports a mismatch between the advertised real-time WebSocket streaming behavior and the inspected non-streaming REST text-to-audio implementation.

Mitigation: Confirm the expected behavior before use; the publisher should implement true WebSocket streaming or relabel the skill as a REST text-to-audio file generator.

Risk: Input text is sent to MiniMax under the user's API key.

Mitigation: Use only non-sensitive text that is appropriate to send to MiniMax, and review MiniMax account and data-handling obligations before use.

Risk: The script writes generated audio to a fixed MP3 path in a local workspace.

Mitigation: Run it in a non-shared, non-privileged workspace and check output-file handling before using it with important local files.

Risk: The shell script constructs JSON with user-provided text.

Mitigation: Avoid untrusted or complex free-form input until the publisher adds JSON-safe request construction.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/ogdegenblaze/skills/kai-realtime-voice)
- [MiniMax text-to-audio API endpoint](https://api.minimax.io/v1/t2a_v2)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Files]

**Output Format:** [Markdown usage guidance with bash commands; generated audio is saved as MP3 by the script.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires MINIMAX_API_KEY; writes realtime_test.mp3 to KAI_MINIMAX_WORKSPACE or the default OpenClaw workspace.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
