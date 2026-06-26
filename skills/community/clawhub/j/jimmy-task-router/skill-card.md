## Description: <br>
Automatically routes tasks to the appropriate tool, agent, or workflow by analyzing task intent and complexity for coding, research, trading, system, content, or general workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jimmyclanker](https://clawhub.ai/user/jimmyclanker) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators can use this skill as a local pre-processor that classifies incoming task text and suggests a matching workflow or tool category. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Routing suggestions could be over-trusted when connected to trading, deployment, scheduling, or other action-capable workflows. <br>
Mitigation: Require explicit confirmation, allowlists, and separate checks for sensitive or destructive requests before using routing output to trigger action-capable agents. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Plain text command-line output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs a route, confidence score, reason, complexity label, and suggested tool.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
