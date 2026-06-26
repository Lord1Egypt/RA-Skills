## Description: <br>
Run structured multi-step workflows via FlowForge engine. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kagura-agent](https://clawhub.ai/user/kagura-agent) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use FlowForge to run YAML-defined, stateful workflows for multi-step tasks that need enforced ordering, branching, and resumable progress. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can broaden its own activation rules by editing SKILL.md trigger text. <br>
Mitigation: Require explicit user approval before changing skill trigger mappings or frontmatter descriptions. <br>
Risk: Workflow YAML can direct the agent to change files, publish branches, or create pull requests. <br>
Mitigation: Review workflow YAML before execution and require approval before repository modifications, branch pushes, or PR creation. <br>
Risk: FlowForge stores persistent workflow state and reset commands can affect local history under ~/.flowforge. <br>
Mitigation: Back up ~/.flowforge before reset operations and confirm which workflow instance is active before advancing. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/kagura-agent/kagura-flowforge) <br>
- [Publisher Profile](https://clawhub.ai/user/kagura-agent) <br>
- [FlowForge Setup Guide](setup.md) <br>
- [FlowForge YAML Format](references/yaml-format.md) <br>
- [Example Workflows](references/examples/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with YAML examples and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write workflow YAML files, update skill trigger mappings, and record workflow outcomes when directed by the active workflow.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
