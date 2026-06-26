## Description: <br>
Procedural Memory helps an agent save successful recurring workflows as reusable skills and memory logs for future use. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chenjin113](https://clawhub.ai/user/chenjin113) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to capture repeated successful workflows, turn them into reusable skill files, and maintain procedural memory across conversations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Cross-session procedural memory can capture sensitive workflow details in local skill and log files. <br>
Mitigation: Avoid using the skill around secrets, credentials, private business workflows, or regulated data, and review generated skills and logs before relying on them. <br>
Risk: The skill includes broad memory, backup, cleanup, external research, and self-improvement maintenance behavior beyond a normal workflow-memory feature. <br>
Mitigation: Disable or remove autonomous backup, cleanup, external research, and startup or self-improvement maintenance instructions unless they are explicitly needed. <br>
Risk: Generated skills can influence future agent behavior. <br>
Mitigation: Review and scan generated SKILL.md files before deployment or automatic reuse. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/chenjin113/procedural-memory) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown skill files, memory logs, shell commands, and user-facing guidance.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May persist derived workflow summaries to local skill and memory files.] <br>

## Skill Version(s): <br>
1.4.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
