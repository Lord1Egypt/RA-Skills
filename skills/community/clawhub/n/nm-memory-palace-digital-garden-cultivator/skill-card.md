## Description: <br>
Manages digital garden notes, link structures, and health metrics. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[athola](https://clawhub.ai/user/athola) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, documentation maintainers, and knowledge-base curators use this skill to organize digital garden notes, maintain bidirectional links, track content maturity, and plan recurring maintenance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Suggested archive or delete actions could remove useful notes if applied without review. <br>
Mitigation: Review proposed archive, delete, and maintenance actions before applying them to a real digital garden or knowledge base. <br>
Risk: Broad triggers may invoke the skill for generic documentation or curation tasks where a digital garden workflow is not intended. <br>
Mitigation: Confirm the task is about organizing or maintaining a digital garden before relying on its guidance. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/athola/nm-memory-palace-digital-garden-cultivator) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/athola) <br>
- [OpenClaw homepage metadata](https://github.com/athola/claude-night-market/tree/master/plugins/memory-palace) <br>
- [modules/linking-patterns.md](modules/linking-patterns.md) <br>
- [modules/maintenance.md](modules/maintenance.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with tables, YAML examples, and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May suggest archive, delete, or maintenance actions for notes; users should review those actions before applying them to real knowledge bases.] <br>

## Skill Version(s): <br>
1.9.12 (source: server release metadata; artifact frontmatter lists 1.9.8) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
