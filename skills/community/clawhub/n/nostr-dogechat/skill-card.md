## Description: <br>
Bridge to the DogeChat Nostr geohash chat network. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[GreatApe42069](https://clawhub.ai/user/GreatApe42069) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and their agents use this skill to send messages to DogeChat Nostr chat rooms, either in the global #d0ge channel or in local geohash-based channels. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can post public Nostr messages tied to a geohash. <br>
Mitigation: Confirm the exact message before each send and use a coarse geohash when possible. <br>
Risk: The skill stores a local signing identity for posting. <br>
Mitigation: Do not share private keys or personal data, and delete ~/.openclaw/nostr-dogechat/identity.json after use if the retained identity is not wanted. <br>
Risk: The security review verdict is suspicious because posting behavior and retained identity controls require user awareness. <br>
Mitigation: Review before installing and only use it when comfortable with public, relay-based DogeChat/Nostr posting. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/GreatApe42069/nostr-dogechat) <br>
- [DogeChat Heartbeat](HEARTBEAT.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and message text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Messages may be posted publicly to global or geohash-based Nostr channels.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
