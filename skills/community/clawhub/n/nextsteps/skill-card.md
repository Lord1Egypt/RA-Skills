## Description: <br>
Append context-aware next-step suggestions after agent responses, including actionable follow-ups, unfinished tasks from memory, and creative lateral suggestions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cindulasai](https://clawhub.ai/user/cindulasai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to append concise, context-aware next-step suggestions after responses and to surface relevant unfinished work from local project memory. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill persistently records inferred preferences, suggestion history, ignored topics, and backlog items in a local .nextsteps folder. <br>
Mitigation: Add .nextsteps/ to .gitignore, periodically inspect or delete those files, and avoid using the skill where persistent local preference or backlog memory is not acceptable. <br>
Risk: The documented disable behavior stops visible suggestions but does not fully stop passive backlog tracking. <br>
Mitigation: When disabling suggestions, also review or remove .nextsteps/BACKLOG.md, or uninstall the skill if passive tracking is not desired. <br>


## Reference(s): <br>
- [Skill page](https://clawhub.ai/cindulasai/nextsteps) <br>
- [Anti-Pattern Rules](references/ANTI-PATTERNS.md) <br>
- [Category Taxonomy](references/CATEGORIES.md) <br>
- [Cold-Start Bootstrap Protocol](references/COLD-START.md) <br>
- [User Customization Protocol](references/CUSTOMIZATION.md) <br>
- [Security Rules](references/SECURITY.md) <br>
- [Self-Improvement Engine](references/SELF-IMPROVE.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Text, Guidance, Configuration] <br>
**Output Format:** [Markdown or compact text suggestions appended to agent responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create and update local .nextsteps preference, history, and backlog files.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
