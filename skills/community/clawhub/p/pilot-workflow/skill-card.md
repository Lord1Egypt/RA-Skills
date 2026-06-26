## Description: <br>
YAML-defined multi-step workflows with orchestration. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[teoslayer](https://clawhub.ai/user/teoslayer) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to define and run YAML-based multi-step Pilot Protocol workflows with conditional logic, loops, parallel steps, and event-driven triggers across multiple agents. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Workflow execution submits task content to selected Pilot Protocol agents. <br>
Mitigation: Avoid placing secrets, private data, or regulated information in task fields unless the selected agents are trusted for that data. <br>
Risk: YAML workflows can orchestrate multiple remote steps and may target unintended agents. <br>
Mitigation: Review workflow YAML before execution and use trusted agent addresses or tags. <br>
Risk: The skill depends on a running Pilot Protocol daemon and local workflow tools. <br>
Mitigation: Confirm pilotctl is on PATH, the daemon is running, and required parsers such as jq and yq are installed before running workflows. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/teoslayer/pilot-workflow) <br>
- [Pilot Protocol](https://pilotprotocol.network) <br>
- [Pilot Skills](https://teoslayer.github.io/pilot-skills/) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with YAML and bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces workflow definitions and Pilot Protocol command guidance; task content may be submitted to remote agents.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
