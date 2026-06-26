## Description: <br>
Performance anti-pattern scanner -- finds N+1 queries, sync I/O, missing pagination, and memory leaks before they hit production. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[suhteevah](https://clawhub.ai/user/suhteevah) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering teams use PerfGuard to scan Python, JavaScript/TypeScript, Ruby, and Java projects for performance anti-patterns before commit or CI release. It reports file-level findings, severity, recommendations, performance scores, audit reports, hotspots, budgets, and trends. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security verdict is suspicious because license handling is not robust enough for sensitive execution contexts. <br>
Mitigation: Review license token handling before sensitive use; avoid untrusted or manually crafted license tokens and prefer disposable environments for validation. <br>
Risk: Paid features can change repository state by installing or modifying lefthook configuration for pre-commit scanning. <br>
Mitigation: Install hooks only in repositories where persistent pre-commit scanning is intended, and review generated or appended lefthook configuration before committing it. <br>
Risk: Trend analysis checks out recent commits and can disturb an active worktree. <br>
Mitigation: Run trend analysis only in a clean or disposable worktree and verify branch state after the command completes. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/suhteevah/perfguard) <br>
- [Publisher profile](https://clawhub.ai/user/suhteevah) <br>
- [PerfGuard website](https://perfguard.pages.dev) <br>
- [PerfGuard pricing](https://perfguard.pages.dev/#pricing) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Terminal text output and Markdown reports with inline remediation guidance.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Free scans are limited to 5 source files; Pro and Team license tiers enable unlimited scans and additional reporting, hooks, budgets, and trend commands.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
