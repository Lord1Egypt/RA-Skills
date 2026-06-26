## Description: <br>
Python code quality checking and LSP integration using pylsp. Provides code diagnostics, completion, hover tips, and style analysis. Use when: checking Python errors/warnings, getting code completions, viewing function signatures, analyzing code quality, or fixing style issues. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[genify](https://clawhub.ai/user/genify) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to check Python files for diagnostics, request completions and symbol information from pylsp, and generate local code-quality reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Optional auto-fix commands can rewrite Python files in the target path. <br>
Mitigation: Run the skill in a trusted Python environment, keep the project under version control, and review diffs after using --auto-fix, autoflake --in-place, or black on a directory. <br>


## Reference(s): <br>
- [LSP protocol reference](references/lsp-protocol.md) <br>
- [pylsp configuration guide](references/pylsp-config.md) <br>
- [PEP8 code style guide](references/pep8-guide.md) <br>
- [python-lsp-server documentation](https://github.com/python-lsp/python-lsp-server) <br>
- [PEP 8 style guide](https://pep8.org/) <br>
- [ClawHub skill page](https://clawhub.ai/genify/lsp-python) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Console text and Markdown reports with optional JSON-formatted LSP responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Batch checks can write timestamped Markdown reports and optional auto-fix commands can modify Python files.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
