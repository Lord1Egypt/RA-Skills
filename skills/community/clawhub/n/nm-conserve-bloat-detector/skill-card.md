## Description: <br>
Detects codebase bloat via dead code, duplication, complexity, and doc bloat scans. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[athola](https://clawhub.ai/user/athola) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering teams use this skill to scan repositories for cleanup candidates, including dead code, duplicate logic, stale documentation, dependency bloat, and rapid codebase growth. It supports quick heuristic scans, targeted analysis with optional tools, and deeper audit reporting before refactoring or release cleanup. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Cleanup recommendations can incorrectly identify live code, documentation, or configuration as removable. <br>
Mitigation: Treat DELETE and ARCHIVE outputs as review candidates, confirm references and tests manually, and require approval before removal. <br>
Risk: Bulk cleanup can remove useful repository history or working implementation details if acted on without safeguards. <br>
Mitigation: Use dry-run previews and create a backup branch before applying broad code or documentation changes. <br>
Risk: Heuristic and static-analysis findings may include false positives, especially for entry points, generated files, stable libraries, and configuration. <br>
Mitigation: Use the skill's confidence levels, exclusions, and tool corroboration before accepting a cleanup recommendation. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/athola/skills/nm-conserve-bloat-detector) <br>
- [Project homepage](https://github.com/athola/claude-night-market/tree/master/plugins/conserve) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and optional report snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include confidence levels, prioritized cleanup candidates, dry-run commands, and remediation categories such as DELETE, REFACTOR, CONSOLIDATE, ARCHIVE, or INLINE.] <br>

## Skill Version(s): <br>
1.9.13 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
