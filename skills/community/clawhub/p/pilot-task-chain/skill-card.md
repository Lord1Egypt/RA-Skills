## Description: <br>
Chain tasks into sequential pipelines across agents. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[teoslayer](https://clawhub.ai/user/teoslayer) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to build dependent multi-agent workflows where each task's output becomes input for the next task. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Intermediate task results may contain sensitive or prompt-injectable content that is passed to later agents. <br>
Mitigation: Review, summarize, or redact intermediate results before sending them to agents that can store, publish, delete, or modify important data. <br>
Risk: Sequential task chains can carry an incorrect result into later workflow steps. <br>
Mitigation: Check each completed task result before submitting dependent follow-up tasks, especially for workflows that affect external systems or persistent data. <br>


## Reference(s): <br>
- [Pilot Protocol](https://pilotprotocol.network) <br>
- [ClawHub Skill Page](https://clawhub.ai/teoslayer/pilot-task-chain) <br>
- [Publisher Profile](https://clawhub.ai/user/teoslayer) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, guidance, text] <br>
**Output Format:** [Markdown with bash command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the pilotctl binary, jq, the pilot-protocol skill, a running Pilot daemon, and multiple agents with complementary capabilities.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata; artifact frontmatter lists 1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
