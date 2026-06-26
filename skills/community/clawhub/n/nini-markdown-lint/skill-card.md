## Description: <br>
Helps developers set up markdownlint-cli2, pre-commit Markdown checks, repository markdownlint configuration, and horizontal-rule cleanup workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[niracler](https://clawhub.ai/user/niracler) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and repository maintainers use this skill to establish Markdown linting standards, configure pre-commit checks, repair common markdownlint findings, and remove horizontal rules outside YAML frontmatter. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Batch-fix commands can rewrite Markdown files in the target repository. <br>
Mitigation: Start from a clean git state, preview the affected file list, run fixes intentionally, and review the resulting diff before committing. <br>
Risk: Installing the pre-commit hook can block commits until Markdown files satisfy the configured checks. <br>
Mitigation: Install it only in repositories where markdownlint enforcement is desired and run the documented validation commands before committing. <br>
Risk: The horizontal-rule checker is a Bash script and may not run in native Windows shells. <br>
Mitigation: Use Git Bash or WSL on Windows, as the skill documentation specifies. <br>


## Reference(s): <br>
- [Markdown Lint skill page](https://clawhub.ai/niracler/nini-markdown-lint) <br>
- [Release v0.3.0](https://github.com/niracler/skill/releases/tag/v0.3.0) <br>
- [markdownlint-cli2 pre-commit hook](https://github.com/DavidAnson/markdownlint-cli2) <br>
- [Node.js](https://nodejs.org/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown with JSON, YAML, text, and bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include repository-specific markdownlint rule choices, pre-commit configuration, and batch-fix commands.] <br>

## Skill Version(s): <br>
0.3.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
