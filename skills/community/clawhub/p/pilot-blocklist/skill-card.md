## Description: <br>
Maintain and share blocklists of untrusted agents in Pilot Protocol networks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[teoslayer](https://clawhub.ai/user/teoslayer) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators of Pilot Protocol networks use this skill to create, update, list, and enforce persistent blocklists for agents that should not be trusted or allowed to connect. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can persistently revoke trust and block peers in a Pilot Protocol network. <br>
Mitigation: Verify node IDs and hostnames before running commands, and use the skill only when the agent is allowed to modify trust and blocklist state. <br>
Risk: Automated score-based blocking can remove peers without sufficient review or rollback planning. <br>
Mitigation: Add manual review, dry-run output, a blocklist backup, and a clear recovery process before enabling automated enforcement. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/teoslayer/pilot-blocklist) <br>
- [Pilot Protocol homepage](https://pilotprotocol.network) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash code blocks and JSON blocklist examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires pilotctl, jq, the pilot-protocol skill, and a running Pilot Protocol daemon.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
