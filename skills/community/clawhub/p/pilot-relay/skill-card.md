## Description: <br>
Store-and-forward messaging for offline peers over the Pilot Protocol network. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[teoslayer](https://clawhub.ai/user/teoslayer) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use Pilot Relay to send asynchronous, store-and-forward messages to trusted Pilot Protocol peers that may be offline and to retrieve queued messages when peers reconnect. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Clearing the inbox can remove stored messages needed for recovery or audit. <br>
Mitigation: Review, export, or otherwise preserve needed messages before running inbox --clear. <br>
Risk: Relay operations depend on trusting pilotctl and the configured Pilot Protocol relay setup. <br>
Mitigation: Install and use the skill only in environments where pilotctl, the daemon, registry connection, and peer trust relationship are already trusted. <br>


## Reference(s): <br>
- [Pilot Protocol homepage](https://pilotprotocol.network) <br>
- [ClawHub Pilot Relay release](https://clawhub.ai/teoslayer/pilot-relay) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Guidance, Configuration] <br>
**Output Format:** [Markdown with bash command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the pilotctl binary, a running Pilot Protocol daemon, registry connectivity, and trusted sender and recipient peers.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
