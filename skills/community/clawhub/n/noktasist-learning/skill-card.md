## Description: <br>
Guides Noktasist through continuous learning, error handling, tool discovery, memory updates, and commit practices. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[noktanyus](https://clawhub.ai/user/noktanyus) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents and operators use this skill to maintain Noktasist's working memory, capture lessons from errors and new tools, and follow a repeatable diagnostic workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent memory and user, identity, or persona file updates could save sensitive details or unreviewed operational assumptions. <br>
Mitigation: Use a controlled workspace and prohibit saving secrets, credentials, raw logs, or sensitive personal details. <br>
Risk: Operational diagnostics, log inspection, and command execution can expose sensitive data or change systems if performed without consent. <br>
Mitigation: Require explicit approval before command execution, log inspection, identity or user file edits, and git commits. <br>
Risk: Broad git staging can include unrelated or sensitive files. <br>
Mitigation: Review staged files and commit only intended changes instead of relying on blanket staging. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/noktanyus/noktasist-learning) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with inline shell commands and file-path conventions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Instruction-only; may prompt memory file updates, operational diagnostics, and git commits.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
