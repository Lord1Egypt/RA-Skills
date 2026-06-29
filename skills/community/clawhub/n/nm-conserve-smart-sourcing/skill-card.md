## Description: <br>
Selects optimal sources for tool calls, balancing accuracy with token cost before research tasks or when deciding whether a claim needs verification. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[athola](https://clawhub.ai/user/athola) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, researchers, and agent users use this skill to decide when web search and citations are worth the token cost. It guides agents toward sourcing high-value claims and using uncertainty notes for lower-value claims. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can influence when an agent chooses to browse or cite sources, which may lead to under-sourcing broadly worded research or accuracy-sensitive tasks. <br>
Mitigation: Review the skill before deployment and require full sourcing for security, compliance, legal, permanent documentation, and research tasks. <br>
Risk: The referenced upstream plugin may include additional agents, hooks, commands, or scripts outside this markdown-only skill. <br>
Mitigation: Review the upstream plugin separately before installing it; this release evidence only reports the packaged skill as markdown-only. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/athola/skills/nm-conserve-smart-sourcing) <br>
- [OpenClaw Homepage](https://github.com/athola/claude-night-market/tree/master/plugins/conserve) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, text] <br>
**Output Format:** [Markdown guidance with citation and uncertainty examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Markdown-only skill; no executable behavior reported by security evidence.] <br>

## Skill Version(s): <br>
1.9.13 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
