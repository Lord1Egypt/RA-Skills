## Description: <br>
Pilot Discover helps agents discover Pilot Protocol peers by tags, polo score, status, hostname, or node ID. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[teoslayer](https://clawhub.ai/user/teoslayer) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to search the Pilot Protocol overlay network for peers with specific capabilities, quality scores, hostnames, or node identifiers. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Running the workflow example can contact a discovered peer through lookup and ping. <br>
Mitigation: Run the skill only with trusted Pilot Protocol, pilotctl, and daemon configurations, and review target peers before issuing lookup or ping commands. <br>
Risk: The skill depends on pilotctl, a running Pilot Protocol daemon, registry access, and jq for the filtering example. <br>
Mitigation: Confirm required tools and daemon access are available before using the command examples. <br>


## Reference(s): <br>
- [Pilot Protocol](https://pilotprotocol.network) <br>
- [Pilot Discover on ClawHub](https://clawhub.ai/teoslayer/pilot-discover) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Markdown with inline bash code blocks and command guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Examples use JSON output from pilotctl and may require jq for filtering.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
