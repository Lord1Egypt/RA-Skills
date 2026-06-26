## Description: <br>
Structured planning mode for performing systematic planning before complex tasks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhaobod1](https://clawhub.ai/user/zhaobod1) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to plan multi-step work before execution, including clarifying requirements, inspecting relevant code, identifying risks, and presenting a concrete plan for confirmation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill encourages the agent to read project files while planning changes. <br>
Mitigation: Keep use scoped to intended workspaces and review the generated plan before authorizing edits. <br>
Risk: A proposed plan could be incomplete, incorrect, or misaligned with the user's intent. <br>
Mitigation: Require user confirmation before execution and verify the plan against the relevant project files and tests. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zhaobod1/huo15-openclaw-plan-mode) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown] <br>
**Output Format:** [Markdown plan with sections for background, steps, risks, and verification] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Instruction-only skill; no external tools or binaries are required by the release evidence.] <br>

## Skill Version(s): <br>
1.0.3 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
