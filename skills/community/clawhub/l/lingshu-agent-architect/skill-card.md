## Description: <br>
灵枢·Agent设计师 helps users design industry-specific AI Agent plans, create runnable baseline agents from configuration and skill packages, and plan enterprise multi-agent systems. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[perrykono-debug](https://clawhub.ai/user/perrykono-debug) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, consultants, and teams use this skill to turn industry or company requirements into AI Agent scenario outlines, MVP plans, OpenClaw configuration guidance, and optional skill publication steps. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill includes broad triggers for designing, creating, and publishing agents, which can lead to unintended changes if the target or version is unclear. <br>
Mitigation: Require an explicit target repository, version, destination, diff review, and final confirmation before any publish step. <br>
Risk: The documented publication flow includes a force-push command that can rewrite remote history. <br>
Mitigation: Avoid the force-push path unless the user deliberately intends to rewrite remote history and confirms after reviewing the diff. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/perrykono-debug/lingshu-agent-architect) <br>
- [Publisher profile](https://clawhub.ai/user/perrykono-debug) <br>
- [README](artifact/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with structured outlines, file templates, JSON configuration examples, and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce workspace file plans and publication command guidance; user review is required before publishing or force-pushing.] <br>

## Skill Version(s): <br>
1.4.0 (source: server release evidence, root SKILL.md frontmatter, README, and _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
