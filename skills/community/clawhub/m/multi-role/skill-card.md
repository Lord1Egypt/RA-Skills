## Description: <br>
multi-role provides a multi-role agent governance workflow that routes complex work across manager, product, engineering, testing, CTO, content, and assistant roles with SOPs, quality gates, task tracking, and project memory. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wzm232803119-arch](https://clawhub.ai/user/wzm232803119-arch) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and teams use this skill to coordinate complex agent work through specialized roles, structured task routing, quality checks, and persistent project records for software delivery, content work, troubleshooting, and operations tasks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can coordinate broad file-reading, file-editing, and sub-agent execution. <br>
Mitigation: Use it only in a clearly scoped project directory and ask it to summarize files read, files modified, and commands run after important tasks. <br>
Risk: The skill keeps persistent project records, including sessions, task logs, archives, and metrics files. <br>
Mitigation: Avoid placing secrets in prompts or logs, and periodically review or delete generated records that are no longer needed. <br>
Risk: Without project-scoped memory isolation, records from multiple projects may be mixed during recall. <br>
Mitigation: Use separate project directories or the documented memory-index companion workflow when working across multiple projects. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wzm232803119-arch/multi-role) <br>
- [README](README.md) <br>
- [Skill definition](SKILL.md) <br>
- [Output rules](OUTPUT-RULES.md) <br>
- [Skill value report specification](SKILL-VALUE-REPORT-SPEC.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown responses with optional code blocks, shell commands, configuration snippets, JSONL records, and project memory files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update session logs, task records, archives, metrics, and project memory files inside the skill workspace.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
