## Description: <br>
Verify agent identity and reputation before interacting with Pilot Protocol nodes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[teoslayer](https://clawhub.ai/user/teoslayer) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to check Pilot Protocol agent identity, reputation scores, and reachability before trusting or connecting to a node. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill depends on pilotctl, jq, and timeout being present and trusted, while only pilotctl is declared in metadata. <br>
Mitigation: Install pilotctl from the legitimate Pilot Protocol project and install jq and timeout from trusted system packages before using the examples. <br>
Risk: Verification results depend on querying a running Pilot daemon and reachable network peers. <br>
Mitigation: Confirm the daemon is running and treat unreachable peers or missing identity data as a failed verification. <br>


## Reference(s): <br>
- [Pilot Protocol](https://pilotprotocol.network) <br>
- [ClawHub package page](https://clawhub.ai/teoslayer/pilot-verify) <br>
- [Publisher profile](https://clawhub.ai/user/teoslayer) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces command examples and verification workflow guidance for pilotctl, jq, and timeout.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
