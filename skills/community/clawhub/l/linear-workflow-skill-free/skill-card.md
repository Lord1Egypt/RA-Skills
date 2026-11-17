## Description: <br>
Linear Workflow Skill Free helps agents use a Node CLI with the Linear API to query teams, projects, and issues, create or update issues, and add comments. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, team leads, and project contributors use this skill to inspect Linear work items, create issues, update status or priority, and record collaboration comments during project management workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requests exec access and a Linear API key for create, update, and comment actions, which can change project data. <br>
Mitigation: Use a dedicated least-privilege Linear API key, query target resources before writes, and confirm every create, update, or comment action before execution. <br>
Risk: The release evidence flags under-scoped and internally inconsistent wording around export, import, delete, save, and convert behavior. <br>
Mitigation: Do not rely on those operations unless the publisher provides a clear CLI implementation and safeguards. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/thcjp/skills/linear-workflow-skill-free) <br>
- [Publisher Profile](https://clawhub.ai/user/thcjp) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include Linear query results, issue update guidance, execution logs, and error summaries.] <br>

## Skill Version(s): <br>
1.0.0 (source: release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
