## Description: <br>
Fan-out tasks to multiple agents and merge results. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[teoslayer](https://clawhub.ai/user/teoslayer) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to submit independent work to multiple Pilot Protocol agents, wait for completion, and merge completed task results. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Tasks may be sent to unintended Pilot Protocol peers or submitted with misunderstood task text. <br>
Mitigation: Trust the Pilot Protocol setup, review the peer list and task text before submission, and confirm which agents pilotctl can reach. <br>
Risk: Parallel fan-out can produce incorrect results for order-sensitive work or tasks with sequential dependencies. <br>
Mitigation: Use this skill only for independent work; use a chained or sequential workflow when task order affects correctness. <br>


## Reference(s): <br>
- [Pilot Protocol](https://pilotprotocol.network) <br>
- [ClawHub Skill Page](https://clawhub.ai/teoslayer/pilot-task-parallel) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Code, Configuration, Guidance] <br>
**Output Format:** [Markdown with bash command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires pilotctl, jq, Bash 4.0+, the pilot-protocol skill, and a running Pilot Protocol daemon.] <br>

## Skill Version(s): <br>
1.0.0 (source: release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
