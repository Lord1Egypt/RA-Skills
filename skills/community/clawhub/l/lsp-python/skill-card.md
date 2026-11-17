## Description:

Python code quality checking and LSP integration using pylsp. Provides code diagnostics, completion, hover tips, and style analysis. Use when: checking Python errors/warnings, getting code completions, viewing function signatures, analyzing code quality, or fixing style issues.

This skill is ready for commercial/non-commercial use.

## Publisher:

[genify](https://clawhub.ai/user/genify)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to inspect Python files and projects for diagnostics, completions, hover information, definitions, and style issues. It can also generate Markdown code-quality reports and optionally apply formatting fixes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The auto-fix workflow can rewrite Python files under the selected path.

Mitigation: Use auto-fix only on version-controlled or backed-up files and review diffs before keeping the changes.

Risk: Install commands use unpinned Python packages.

Mitigation: Install in a virtual environment and review or pin dependencies before use.

## Reference(s):

- [LSP protocol reference](references/lsp-protocol.md)
- [pylsp configuration guide](references/pylsp-config.md)
- [PEP 8 style guide](references/pep8-guide.md)
- [Language Server Protocol](https://microsoft.github.io/language-server-protocol/)
- [Python LSP Server](https://github.com/python-lsp/python-lsp-server)
- [PEP 8](https://pep8.org/)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands; scripts emit plain text diagnostics, JSON LSP responses, and Markdown reports.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Optional auto-fix mode can rewrite Python files and produce a timestamped report.]

## Skill Version(s):

1.1.0 (source: server release metadata, created 2026-03-01)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
