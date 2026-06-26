## Description: <br>
Polo score escrow for verified task completion. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[teoslayer](https://clawhub.ai/user/teoslayer) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators using Pilot Protocol use this skill to create, verify, release, and dispute polo score escrow for task workflows where rewards should be held until completion is verified. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Escrow commands may affect real pilot-protocol rewards, completion claims, disputes, or releases. <br>
Mitigation: Before approving create, dispute, or release actions, confirm the escrow agent, executor, amount, task data, escrow ID, and network environment. <br>
Risk: The workflow depends on a trusted escrow agent and correct network state. <br>
Mitigation: Use a trusted escrow agent, verify pilotctl output before acting, and include an arbiter when dispute resolution is needed. <br>


## Reference(s): <br>
- [Pilot Protocol](https://pilotprotocol.network) <br>
- [Pilot Escrow on ClawHub](https://clawhub.ai/teoslayer/pilot-escrow) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown with bash command examples and JSON payloads] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires pilotctl, jq, a trusted escrow agent, and explicit user review before live escrow actions.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
