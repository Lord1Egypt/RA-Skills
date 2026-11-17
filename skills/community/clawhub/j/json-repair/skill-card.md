## Description:

JSON修复工具 helps agents repair JSON-like files by using Node.js parsing to normalize trailing commas, single quotes, unquoted keys, comments, and hex or octal numbers into valid JSON.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to repair malformed JSON-like configuration or data files and return validated JSON through an agent workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requests command execution and file-write authority for JSON repair tasks.

Mitigation: Limit use to explicit file paths in a small trusted scope, review commands before execution, and keep backups enabled.

Risk: Recursive repair and overwrite options can modify many files or remove recovery paths.

Mitigation: Avoid recursive runs unless the target directory is reviewed first, and treat any no-backup mode as high risk.

Risk: JavaScript-based parsing can be unsafe for untrusted or malicious input.

Mitigation: Use only trusted JSON-like files unless the implementation uses a dedicated non-executing parser, and validate repaired output before writing it.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/json-repair)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON-oriented output descriptions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose file reads, file writes, command execution, backups, and validation steps.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
