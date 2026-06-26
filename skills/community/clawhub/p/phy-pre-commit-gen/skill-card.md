## Description: <br>
Generates a tailored .pre-commit-config.yaml by analyzing a project's language stack, linting tools, and CI setup, and can audit existing pre-commit configs for unpinned revisions and missing security hooks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[PHY041](https://clawhub.ai/user/PHY041) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to generate or audit pre-commit configurations tailored to a repository's language stack, linting tools, and CI setup. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated pre-commit configuration may replace or change an existing repository workflow. <br>
Mitigation: Use --dry-run first, review the generated .pre-commit-config.yaml, and use --overwrite only when intentionally replacing an existing config. <br>
Risk: Running pre-commit after generation may fetch pinned hook repositories and allow formatters to modify project files. <br>
Mitigation: Run pre-commit from a clean working tree, review hook revisions, and inspect file changes before committing. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/PHY041/phy-pre-commit-gen) <br>
- [Canlah AI homepage](https://canlah.ai) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with bash examples and generated .pre-commit-config.yaml content] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can preview output with --dry-run, audit an existing config, or write a .pre-commit-config.yaml when file-writing options are used.] <br>

## Skill Version(s): <br>
1.0.3 (source: server evidence and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
