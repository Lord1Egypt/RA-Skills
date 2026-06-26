## Description: <br>
Static code smell detector for Python, JavaScript/TypeScript, Java, Go, and Ruby that reports structural anti-patterns with severity, line-level findings, and refactoring suggestions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[PHY041](https://clawhub.ai/user/PHY041) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering teams use this skill to audit source repositories for structural code quality issues before refactoring, review, or CI gating. It is intended for local analysis of supported Python, JavaScript/TypeScript, Java/Kotlin, Go, and Ruby files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The scanner can include source snippets, file paths, and line-level findings in its output. <br>
Mitigation: Run it only against the intended repository or a narrow --root path, and review reports before sharing them outside the project. <br>
Risk: Static heuristic findings may include false positives or miss context-specific issues. <br>
Mitigation: Treat findings as review prompts and confirm suggested refactors with project maintainers and tests before changing code. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/PHY041/phy-code-smell) <br>
- [Canlah AI homepage](https://canlah.ai) <br>
- [Publisher profile](https://clawhub.ai/user/PHY041) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown report with severity-grouped findings, file paths, line numbers, metrics, refactoring suggestions, and optional CI command guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can be scoped with --root and filtered with --min-severity; threshold behavior can be adjusted with documented environment variables.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
