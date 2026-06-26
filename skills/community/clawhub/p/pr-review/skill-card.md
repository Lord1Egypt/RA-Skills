## Description: <br>
Finds and fixes code issues before publishing a PR, using a single-pass review with auto-fix for code changes and existing-code audits. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Glucksberg](https://clawhub.ai/user/Glucksberg) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to review branch changes before opening a PR or audit selected code for bugs, security issues, reliability gaps, performance issues, and quality problems. It can apply high-confidence fixes directly and reports remaining issues for manual review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may modify repository files while applying auto-fixes. <br>
Mitigation: Use it on a clean branch or clean working tree, then review git diff and run tests before committing or opening a PR. <br>
Risk: Automated review findings and fixes may be incomplete or incorrect. <br>
Mitigation: Treat the report and any edits as review inputs, verify the changed code manually, and keep ambiguous fixes for human review. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Glucksberg/pr-review) <br>
- [Pre-Review Skill README](artifact/plugins/pre-review/README.md) <br>
- [Pre-Review command](artifact/plugins/pre-review/commands/pre-review.md) <br>
- [Code Audit command](artifact/plugins/pre-review/commands/code-audit.md) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Markdown, Code, Shell commands, Guidance] <br>
**Output Format:** [Markdown reports with file edits and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May modify repository files when high-confidence fixes meet the configured threshold.] <br>

## Skill Version(s): <br>
2.0.1 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
