## Description: <br>
Guides an agent to use ripgrep or grep to locate code symbols, definitions, usages, configuration, and errors before reading files. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhaobod1](https://clawhub.ai/user/zhaobod1) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and coding agents use this skill to find definitions, usages, configuration sources, error origins, and affected files before reading or editing code. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Code searches may surface API keys, credentials, or other sensitive strings from the local repository. <br>
Mitigation: Treat search results as potentially sensitive and avoid sharing matches externally when they contain secrets or private implementation details. <br>
Risk: A single broad or isolated search result can lead to incorrect conclusions about code ownership, behavior, or impact. <br>
Mitigation: Narrow searches by directory, file type, and pattern, then follow definitions, usages, and tests before drawing conclusions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zhaobod1/skills/huo15-grep) <br>
- [Skill-supplied homepage](https://github.com/zhaobod1/huo15-skills) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with ripgrep or grep command examples and file:line findings] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Emphasizes read-only search, narrowing broad results, following definition-to-usage chains, and reporting precise file and line locations.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
