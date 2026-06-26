## Description: <br>
Heleni Memory Architecture guides PA agents in maintaining long-term memory with fact and deduction tagging, session summaries, project memory files, and memory compaction. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[netanel-abergel](https://clawhub.ai/user/netanel-abergel) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agent developers use this skill to guide PA agents that maintain MEMORY.md, daily logs, project memory files, and recurring memory review workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Suggested recurring review jobs may rewrite memory and agent-instruction files or commit changes without continuous human review. <br>
Mitigation: Enable the crons only when unattended edits are acceptable, require human review before commits or pushes, and audit affected files regularly. <br>
Risk: Deduced memories can encode incorrect or stale assumptions about a user. <br>
Mitigation: Keep secrets out of memory files, label inferred entries clearly, and periodically review or remove [DEDUCED] memories that are unsupported or outdated. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/netanel-abergel/heleni-memory-architecture) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with inline shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May update memory files, agent instruction files, and git history when its suggested review and compaction workflows are enabled.] <br>

## Skill Version(s): <br>
1.0.0 (source: release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
