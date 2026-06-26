## Description: <br>
Meta Skill Weaver helps agents decompose complex multi-step tasks, coordinate multiple skills with event-driven orchestration, manage progress and recovery, and collect metrics and feedback. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pagoda111king](https://clawhub.ai/user/pagoda111king) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, advanced users, and teams use this skill to orchestrate long-running workflows that require task decomposition, multi-skill coordination, progress tracking, timeout handling, and resumption after interruption. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: High-authority orchestration can coordinate file- and command-capable tools in multi-step tasks. <br>
Mitigation: Review planned actions before execution and use explicit task IDs and commands for resume or status operations. <br>
Risk: Metrics and feedback middleware can store task IDs, comments, and operational data locally. <br>
Mitigation: Do not put secrets or sensitive personal data in feedback comments or task IDs, and review storage paths before deployment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/pagoda111king/meta-skill-weaver) <br>
- [Skill documentation](https://clawhub.ai/skills/meta-skill-weaver/docs) <br>
- [Skill issue tracker](https://clawhub.ai/skills/meta-skill-weaver/issues) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and code snippets, plus workflow guidance and orchestration reports.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May persist local metrics and feedback data in configured storage paths.] <br>

## Skill Version(s): <br>
2.5.0 (source: server release metadata and package.json; SKILL.md frontmatter lists 2.4.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
