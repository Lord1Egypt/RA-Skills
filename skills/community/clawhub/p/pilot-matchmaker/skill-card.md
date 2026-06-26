## Description: <br>
Match agents with complementary capabilities for capability requirements, collaborative workflows, resource pooling, or team building. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[teoslayer](https://clawhub.ai/user/teoslayer) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and agent operators use this skill to discover and rank Pilot Protocol agents by capability, trust, latency, pricing, and SLA fit when selecting collaborators or building agent teams. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill relies on pilotctl and a running Pilot Protocol daemon to query peer discovery, trust, lookup, and latency data. <br>
Mitigation: Install and run it only in environments where pilotctl and the daemon are trusted, and review generated commands before execution. <br>
Risk: Matchmaking results can be misleading if peer trust, latency, pricing, or SLA data is stale or incomplete. <br>
Mitigation: Validate selected agents with independent checks before using them in production workflows. <br>


## Reference(s): <br>
- [Pilot Protocol](https://pilotprotocol.network) <br>
- [ClawHub Skill Page](https://clawhub.ai/teoslayer/pilot-matchmaker) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, code] <br>
**Output Format:** [Markdown with Bash command examples and script snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires pilotctl, a running Pilot Protocol daemon, jq, and bc.] <br>

## Skill Version(s): <br>
1.0.0 (source: release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
