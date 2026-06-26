## Description: <br>
Keep Learning Agent helps agents record, index, refine, and promote reusable learning records, SOPs, and maintenance guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chow651](https://clawhub.ai/user/chow651) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent operators use this skill to maintain structured learning records, quick indexes, issue states, and reusable solution patterns for an AI agent. It is intended for environments where users want agent memory and process improvements to be persisted and reviewed over time. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill describes running local PowerShell maintenance scripts that may be unreviewed in the user's environment. <br>
Mitigation: Inspect or disable the referenced PowerShell scripts before enabling automated startup or repair behavior. <br>
Risk: Learning records may be promoted into global agent configuration without enough scoping or user control. <br>
Mitigation: Keep learning files in a scoped directory and manually review any content before promoting it into AGENTS.md or other global configuration. <br>
Risk: Persistent learning logs could accidentally store sensitive information. <br>
Mitigation: Avoid storing secrets, credentials, private user data, or confidential operational details in learning records. <br>


## Reference(s): <br>
- [Keep Learning Agent on ClawHub](https://clawhub.ai/chow651/keep-learning-agent) <br>
- [README.md](artifact/README.md) <br>
- [SKILL.md](artifact/SKILL.md) <br>
- [_meta.json](artifact/_meta.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with command examples, templates, and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose persistent learning files and local PowerShell or Python maintenance steps that should be reviewed before use.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter, _meta.json, release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
