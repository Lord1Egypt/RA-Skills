## Description: <br>
Deploys a four-agent Pilot content distribution setup with one origin and three regional edge nodes for replicated updates and heartbeat monitoring. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[teoslayer](https://clawhub.ai/user/teoslayer) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to configure a Pilot origin and regional edge agents for content replication, trust handshakes, host naming, and heartbeat monitoring. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Incorrect role, prefix, peer hostname, or manifest path can configure agents for the wrong replication topology. <br>
Mitigation: Confirm the role, deployment prefix, peer hostnames, and ~/.pilot manifest path before applying the setup. <br>
Risk: Cross-host handshakes establish trust between Pilot agents. <br>
Mitigation: Handshake only with hosts you control or trust, then verify trust state before sending content updates. <br>
Risk: The setup depends on pilot-* skills plus the pilotctl and clawhub binaries. <br>
Mitigation: Review the named skills and install pilotctl and clawhub only from trusted sources. <br>


## Reference(s): <br>
- [Pilot Protocol homepage](https://pilotprotocol.network) <br>
- [ClawHub skill page](https://clawhub.ai/teoslayer/pilot-multi-region-content-sync-setup) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON manifest templates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes role-specific hostnames, peer lists, data flows, handshake steps, and dependency requirements.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
