## Description: <br>
Plan, orchestrate, and adversarially verify parallel AI coding agents with a local Open Dynamic Workflows daemon. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[suraj1235](https://clawhub.ai/user/suraj1235) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to plan, run, and collect results from multi-agent coding workflows when tasks can be split into parallel work and require adversarial verification. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The daemon uses model-provider credentials and can access the project directory. <br>
Mitigation: Install and run it only in trusted environments, keep credentials in environment variables or local configuration, and do not place provider keys in prompts or source files. <br>
Risk: Workflow execution may request file writes, shell commands, or git operations. <br>
Mitigation: Review the daemon approval settings and require explicit authorization before any non-read-only operation. <br>
Risk: Long-running parallel workflows can consume tokens, time, and cost. <br>
Mitigation: Confirm the generated topology, agent count, cost estimate, and hard limits before execution, and enforce the per-workflow budget. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/suraj1235/open-dynamic-workflows) <br>
- [Publisher profile](https://clawhub.ai/user/suraj1235) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, JSON, files] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON daemon responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires node and ANTHROPIC_API_KEY; uses a local daemon on 127.0.0.1 and may write plan.json.] <br>

## Skill Version(s): <br>
0.1.0 (source: SKILL.md frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
