## Description: <br>
Guides an agent in managing MaxClaw internal IM and OpenClaw support skills, including when to suggest installing or updating related official skills. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oreoandyuumi](https://clawhub.ai/user/oreoandyuumi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to identify when related IM and OpenClaw management skills should be installed or updated. The skill emphasizes asking for user confirmation before running install or update commands. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A downstream skill described as official may not be from a trusted publisher. <br>
Mitigation: Verify the publisher of each downstream skill before approving installation or update. <br>
Risk: A downstream skill may request unexpected credentials, broad filesystem access, or unrelated capabilities. <br>
Mitigation: Review requested permissions and capabilities before approving any install or update command. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/oreoandyuumi/mmxagent-skill-manager) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration instructions] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Instruction-only skill; downstream install or update commands require user approval before execution.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
