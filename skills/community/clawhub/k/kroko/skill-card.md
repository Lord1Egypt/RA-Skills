## Description:

Use when writing or reviewing code to hard limits.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sakib-dalal](https://clawhub.ai/user/sakib-dalal)

### License/Terms of Use:

MIT

## Use Case:

Developers use KROKO to write, review, or refactor code against explicit size, complexity, recursion, error handling, and documentation limits, and to configure those limits for an agent or repository.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The installer copies KROKO into the default Hermes skill directory and each named profile under HERMES_HOME.

Mitigation: Review the target paths and copied files in install.sh before running it, and use a controlled Hermes home if installation across all profiles is not intended.

Risk: The hook installer persistently writes a Git pre-commit hook and may move an existing hook to a timestamped backup.

Mitigation: Confirm the repository path and inspect its current hook and the KROKO hook template before installing; verify the staged-file checks match the repository's workflow.

Risk: The release includes graphics tools outside its stated code-limit purpose, and the security scan is partial.

Mitigation: Review tools/halftone-core.js and tools/render_logo.html before using them, and treat the scan as incomplete coverage of referenced or partially inspected components.

## Reference(s):

- [Code limits and their sources](references/limits.md)
- [Comment doctrine](references/comment-doctrine.md)
- [Managed-language leak guidance](references/managed-language-leaks.md)
- [Interface gates](references/interface-gates.md)
- [Veracode 2025 GenAI Code Security Report](https://www.veracode.com/press-release/ai-generated-code-poses-major-security-risks-in-nearly-half-of-all-development-tasks-veracode-research-reveals/)
- [GitClear AI Code Quality Research 2025](https://www.gitclear.com/ai_assistant_code_quality_2025_research)

## Skill Output:

**Output Type(s):** [Guidance, Code, Shell commands, Configuration instructions]

**Output Format:** [Markdown with code examples, shell commands, and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes gate findings and limitations when reporting results; passing the gate does not establish that code is correct, secure, or well designed.]

## Skill Version(s):

2.0.0 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
