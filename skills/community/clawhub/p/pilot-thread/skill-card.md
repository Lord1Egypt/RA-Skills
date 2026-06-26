## Description: <br>
Threaded conversations with context tracking over the Pilot Protocol network. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[teoslayer](https://clawhub.ai/user/teoslayer) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to organize multi-turn Pilot Protocol conversations into topic-specific threads with replies, subscriptions, and message history. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill relies on shell commands that publish and subscribe to Pilot Protocol topics. <br>
Mitigation: Review target hostnames, thread topics, and message payloads before running commands. <br>
Risk: The skill depends on local Pilot Protocol tooling and daemon state. <br>
Mitigation: Confirm pilotctl, jq, and the Pilot daemon are installed and trusted before using the workflow. <br>
Risk: Server security guidance recommends using the release only in a trusted development context. <br>
Mitigation: Install and run the skill only where the local tooling and authenticated environment are trusted. <br>


## Reference(s): <br>
- [Pilot Protocol](https://pilotprotocol.network) <br>
- [ClawHub skill page](https://clawhub.ai/teoslayer/pilot-thread) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash code blocks and JSON command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires pilot-protocol, pilotctl on PATH, jq, and a running Pilot daemon.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
