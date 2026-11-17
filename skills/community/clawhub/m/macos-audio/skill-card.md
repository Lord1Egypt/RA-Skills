## Description:

Manage macOS audio output and Bluetooth devices via the macos-audio CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vossenwout](https://clawhub.ai/user/vossenwout)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to have an agent propose macOS audio CLI commands for scanning devices, connecting or disconnecting Bluetooth or AirPlay outputs, switching local outputs, checking status, setting volume, and playing local audio files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Commands can change the active audio output, connect or disconnect Bluetooth devices, change system volume, or play local audio.

Mitigation: Run `macos-audio status` before making changes and only execute disruptive commands when the requested audio change is intended.

Risk: The release depends on Homebrew-installed tools and a third-party tap.

Mitigation: Review the Homebrew tap and install `switchaudio-osx`, `blueutil`, and `macos-audio-cli` from the intended sources before use.

Risk: AirPlay support is documented as experimental and may be unreliable.

Mitigation: Prefer local or Bluetooth output routing when reliability is required, and verify the selected output after any AirPlay command.

## Reference(s):


## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands and CLI status guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include JSON status command usage when recommending machine-readable audio state checks.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
