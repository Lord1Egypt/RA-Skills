## Description: <br>
New Agent Onboarding provides a training manual that teaches agents workspace management, user communication, error handling, tool-use practices, and self-improvement routines. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[harrot90-code](https://clawhub.ai/user/harrot90-code) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to onboard new agents with consistent behavior expectations, communication rules, local-memory practices, and review routines. It is most relevant when creating or supervising sub-agents that need a shared training manual. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill teaches agents to maintain local memory and user-profile files that may contain private user context. <br>
Mitigation: Confirm which local agent folders may be changed before use, and do not copy USER.md or similar profile files into sub-agent workspaces unless the user has approved that scope. <br>
Risk: Training workflows can lead agents to create or update sub-agent configuration and memory files. <br>
Mitigation: Apply changes only inside explicitly authorized agent workspaces and review generated file changes before deploying trained agents. <br>


## Reference(s): <br>
- [Training manual template](artifact/references/training-manual-template.md) <br>
- [ClawHub skill page](https://clawhub.ai/harrot90-code/new-agent-onboarding) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Configuration instructions] <br>
**Output Format:** [Markdown guidance and training templates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May guide agents to create or update local agent memory, profile, and training files.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
