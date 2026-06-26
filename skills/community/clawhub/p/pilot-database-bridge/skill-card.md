## Description: <br>
Query remote databases through Pilot Protocol tunnels. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[teoslayer](https://clawhub.ai/user/teoslayer) <br>

### License/Terms of Use: <br>
AGPL-3.0 <br>


## Use Case: <br>
Developers and agent builders use this skill to open Pilot Protocol tunnels to remote PostgreSQL, MySQL, MongoDB, and Redis databases when direct network access is unavailable. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Database tunnels can expose sensitive remote database access if mapped broadly or used with privileged credentials. <br>
Mitigation: Use least-privilege or read-only database accounts, confirm mapped hosts before connecting, avoid broad production access, and stop the gateway when finished. <br>


## Reference(s): <br>
- [Pilot Protocol](https://pilotprotocol.network) <br>
- [ClawHub skill page](https://clawhub.ai/teoslayer/pilot-database-bridge) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with bash command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands use pilotctl JSON mode and require the Pilot daemon, gateway, and relevant database clients.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
