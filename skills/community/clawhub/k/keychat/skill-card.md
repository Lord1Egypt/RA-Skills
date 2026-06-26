## Description: <br>
Install Keychat - sovereign E2E encrypted messaging for OpenClaw agents via Signal Protocol over Nostr relays. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kcdev001](https://clawhub.ai/user/kcdev001) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to install Keychat messaging for an agent, configure the OpenClaw gateway, and connect through encrypted Keychat contacts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Installing the skill gives the agent a persistent Keychat/Nostr messaging identity. <br>
Mitigation: Install only when the agent should receive Keychat messaging access, and run setup from a private chat or trusted environment. <br>
Risk: The plugin uses local keychain storage and a sidecar process for its messaging bridge. <br>
Mitigation: Review the third-party plugin source or package provenance when the deployment has a strict threat model. <br>


## Reference(s): <br>
- [Keychat OpenClaw homepage](https://github.com/keychat-io/keychat-openclaw) <br>
- [Keychat app](https://keychat.io) <br>
- [ClawHub skill page](https://clawhub.ai/kcdev001/keychat) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash code blocks and setup guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May guide installation that creates a persistent Keychat/Nostr messaging identity, starts a sidecar process, and stores identity material in the OS keychain.] <br>

## Skill Version(s): <br>
1.1.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
