## Description: <br>
Detects codebase bloat via dead code, duplication, complexity, and documentation bloat scans. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[athola](https://clawhub.ai/user/athola) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and maintainers use this skill to audit codebases for dead code, duplication, complexity, documentation bloat, dependency bloat, stale files, and growth patterns before cleanup, refactoring, or release work. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Deep scans may inspect broad portions of a repository and may query package registries for dependency checks. <br>
Mitigation: Run targeted or dry-run scans first, review proposed commands, and avoid scanning sensitive paths that are not needed for the audit. <br>
Risk: Cleanup recommendations may include deleting, archiving, or modifying files. <br>
Mitigation: Apply remediation only after reviewing diffs on a branch or with equivalent version-control safeguards. <br>
Risk: Static and heuristic bloat findings can produce false positives. <br>
Mitigation: Treat findings as candidates, confirm usage and test coverage, and prefer high-confidence removals for automated cleanup. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/athola/nm-conserve-bloat-detector) <br>
- [Publisher profile](https://clawhub.ai/user/athola) <br>
- [Skill homepage](https://github.com/athola/claude-night-market/tree/master/plugins/conserve) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown analysis with command snippets and remediation recommendations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Findings are confidence-ranked and may include dry-run cleanup guidance.] <br>

## Skill Version(s): <br>
1.9.12 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
