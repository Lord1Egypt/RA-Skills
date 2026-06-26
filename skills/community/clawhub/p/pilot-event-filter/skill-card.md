## Description: <br>
Filters and transforms Pilot Protocol event streams before delivery using pattern matching and jq transforms. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[teoslayer](https://clawhub.ai/user/teoslayer) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators working with Pilot Protocol event streams use this skill to filter, transform, and conditionally forward events so agents receive only relevant payloads. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: jq filters or publish destinations can forward event contents to unintended agents. <br>
Mitigation: Review jq filters, subscribed topics, and publish destinations before running examples. <br>
Risk: Commands depend on the local Pilot Protocol daemon, pilotctl, and jq environment. <br>
Mitigation: Install only in trusted Pilot Protocol environments with required binaries available and the daemon running. <br>


## Reference(s): <br>
- [Pilot Protocol](https://pilotprotocol.network) <br>
- [ClawHub skill page](https://clawhub.ai/teoslayer/pilot-event-filter) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with bash command examples and jq expressions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires pilotctl, jq, the pilot-protocol skill, and a running Pilot Protocol daemon.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
