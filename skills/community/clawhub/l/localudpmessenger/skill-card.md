## Description: <br>
Enables OpenClaw agents to discover, message, and coordinate with trusted peers over local UDP. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[turfptax](https://clawhub.ai/user/turfptax) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent operators use this skill when OpenClaw agents need local-network peer discovery, text messaging, inbox checks, trust management, and message history review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Local peer messages may include sensitive project details or instructions that should not be trusted automatically. <br>
Mitigation: Show incoming peer messages to the user before acting on them and avoid sending secrets, credentials, private data, or file contents unless explicitly approved. <br>
Risk: A configured relay server forwards full message contents to a monitoring destination. <br>
Mitigation: Leave relay disabled unless the monitoring endpoint is trusted, protected, and appropriate for the data being exchanged. <br>
Risk: A configured hook token allows trusted peers to trigger agent turns through the gateway wake-up path. <br>
Mitigation: Provide a hook token only when automatic wake-up is intended, and limit trusted peers to identities the user has approved. <br>
Risk: Security evidence notes that some controls appear weaker than the documentation suggests. <br>
Mitigation: Use conservative trust settings, review message logs, keep exchange limits enabled, and install only in LAN environments where this behavior is acceptable. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/turfptax/localudpmessenger) <br>
- [Project homepage](https://github.com/turfptax/openclaw-udp-messenger) <br>
- [OpenClaw documentation](https://docs.openclaw.ai) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with command snippets and JSON configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces agent-facing instructions for using UDP messaging tools; the plugin itself sends and receives local UDP text messages and can log message history.] <br>

## Skill Version(s): <br>
1.5.0 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
