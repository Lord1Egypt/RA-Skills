## Description: <br>
Publish messages to all trusted peers on a topic over the Pilot Protocol network. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[teoslayer](https://clawhub.ai/user/teoslayer) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers who use Pilot Protocol use this skill to broadcast announcements, status updates, notifications, or alerts to all trusted peers on a topic. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broadcast messages are not private and may be visible to trusted peers subscribed to the topic. <br>
Mitigation: Verify the trust network and intended recipient scope before publishing, and do not include secrets, credentials, personal data, or sensitive internal status in broadcasts. <br>


## Reference(s): <br>
- [Pilot Protocol](https://pilotprotocol.network) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Guidance] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires pilotctl on PATH, a running Pilot daemon, and active trust relationships.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
