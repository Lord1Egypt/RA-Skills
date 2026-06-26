## Description: <br>
Manage macOS audio output and Bluetooth devices via the macos-audio CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[vossenwout](https://clawhub.ai/user/vossenwout) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users on macOS use this skill to inspect audio state, switch audio outputs, manage Bluetooth or AirPlay routing, set volume, and play local audio through the macos-audio CLI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can enable an agent to change live audio routing, Bluetooth connections, volume, and playback. <br>
Mitigation: Review agent requests before allowing connect, disconnect, AirPlay routing, playback, or volume changes, and run macos-audio status first to confirm the current state. <br>
Risk: Installing and using the skill depends on Homebrew packages and the publisher's tap. <br>
Mitigation: Verify that the Homebrew tap and dependencies are trusted before installing them. <br>
Risk: AirPlay routing is documented as experimental and known to be buggy. <br>
Mitigation: Avoid AirPlay routing for critical workflows and verify the selected output after any AirPlay command. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/vossenwout/macos-audio) <br>
- [Publisher profile](https://clawhub.ai/user/vossenwout) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and command output expectations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include JSON status output when the CLI is invoked with status --json.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
