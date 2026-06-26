## Description: <br>
Control Sonos speakers with commands for discovery, status, playback, volume, and grouping. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lovefromio](https://clawhub.ai/user/lovefromio) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and Sonos users use this skill to have an agent provide Sonos CLI commands and setup guidance for discovering speakers, checking status, controlling playback, adjusting volume, managing groups, and using favorites or queues on a local network. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The referenced Go CLI discovers and controls Sonos devices on the user's local network. <br>
Mitigation: Install and run it only on trusted networks, confirm target speaker names or IP addresses before executing commands, and review proposed commands before use. <br>
Risk: Optional Spotify search requires Spotify credentials to be available to the CLI environment. <br>
Mitigation: Provide Spotify credentials only when Spotify search is needed, use credentials you can rotate, and avoid sharing command output or logs that may expose environment details. <br>
Risk: Installing the CLI builds code from the referenced upstream Go module. <br>
Mitigation: Install only if you trust the upstream module and are comfortable building and running that command-line tool in your environment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lovefromio/lovefromio-sonoscli) <br>
- [sonoscli homepage](https://sonoscli.sh) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include local-network troubleshooting guidance and optional Spotify credential setup notes.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
