## Description:

Play TTS or audio on the Raspberry Pi (or gateway host) default speaker.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nobloodontheleaves](https://clawhub.ai/user/nobloodontheleaves)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to have an agent generate a short TTS message or use an existing audio file, then play it through the gateway host's default speaker.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can cause audible playback on the gateway host's default speaker, which may be disruptive in shared or quiet environments.

Mitigation: Install and enable it only on gateways where local speaker playback is intended, and review agent actions before playback.

Risk: Playback depends on local audio tooling and a configured default sink.

Mitigation: Confirm paplay or pw-play is installed and that the target speaker is connected and selected as the default audio output.

## Reference(s):

- [Pi Speaker ClawHub skill page](https://clawhub.ai/nobloodontheleaves/skills/pi-speaker)
- [Raspberry Pi audio setup](/platforms/raspberry-pi-audio)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Guidance]

**Output Format:** [Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guides the agent to generate TTS audio, extract the local audio path, execute playback with paplay, pw-play, or the helper script, and report success only after playback exits successfully.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
