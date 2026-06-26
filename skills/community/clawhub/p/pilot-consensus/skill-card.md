## Description: <br>
Distributed voting and agreement protocols for multi-agent decision making. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[teoslayer](https://clawhub.ai/user/teoslayer) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external agent operators use this skill to coordinate distributed votes, quorum checks, and commit decisions across multiple agents using Pilot Protocol tooling. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Consensus proposals and peer messages can affect real multi-agent coordination decisions. <br>
Mitigation: Review generated pilotctl commands, registry hosts, peer addresses, proposal values, and consensus groups before running them in a live environment. <br>
Risk: The skill depends on external Pilot tooling and a running daemon. <br>
Mitigation: Install pilotctl and the Pilot daemon from a trusted source and verify jq and uuidgen are available before use. <br>


## Reference(s): <br>
- [Pilot Protocol](https://pilotprotocol.network) <br>
- [ClawHub skill page](https://clawhub.ai/teoslayer/pilot-consensus) <br>
- [Publisher profile](https://clawhub.ai/user/teoslayer) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires pilotctl on PATH, a running Pilot daemon, jq, uuidgen, and trusted registry hosts, peers, proposal values, and consensus groups.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
