## Description: <br>
Helps an agent capture lessons, structured retrospectives, and plan logs after non-trivial work, errors, unexpected discoveries, or user requests to record what was learned. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[futurizerush](https://clawhub.ai/user/futurizerush) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to turn completed work, errors, and trial-and-error sessions into reusable lessons, prevention steps, and plan logs that reduce future drift. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can create durable lesson or plan notes about user work without enough consent, scoping, or redaction guidance. <br>
Mitigation: Require explicit confirmation before creating files or memory entries, let the user choose the storage location, and avoid saving secrets, credentials, private paths, customer data, or raw command output. <br>
Risk: Suggested code, CI, tooling, or process changes may be incorrect or unsuitable for a project. <br>
Mitigation: Treat proposed changes as reviewable recommendations and apply normal code, security, and operational review before deployment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/futurizerush/learn-reflect) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown lesson entries, plan logs, and implementation guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose durable prevention changes such as code, checks, directives, or notes for normal review before use.] <br>

## Skill Version(s): <br>
0.2.0 (source: frontmatter and server evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
