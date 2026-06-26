## Description: <br>
Deploy a disaster response coordination system with four agents for sensor aggregation, response coordination, resource allocation, and public communications. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[teoslayer](https://clawhub.ai/user/teoslayer) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and emergency-management operators use this skill to configure a four-agent Pilot disaster-response workflow spanning sensor intake, incident coordination, resource allocation, and communications. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The setup can route live public emergency alerts or agency communications through downstream Pilot skills. <br>
Mitigation: Install first in a staging or isolated Pilot environment and do not connect communications to real broadcast, SMS, Slack, webhook, or agency channels until credentials and destinations have been reviewed. <br>
Risk: The workflow can create persistent Pilot configuration and trust relationships. <br>
Mitigation: Back up existing ~/.pilot configuration, review each downstream pilot-* skill, and verify how to disable or undo handshakes and manifests before production use. <br>


## Reference(s): <br>
- [Pilot Protocol](https://pilotprotocol.network) <br>
- [ClawHub skill page](https://clawhub.ai/teoslayer/pilot-disaster-response-setup) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with bash commands and JSON manifest snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires pilotctl, clawhub, the pilot-protocol skill, downstream pilot skills for the selected role, and a running daemon.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
