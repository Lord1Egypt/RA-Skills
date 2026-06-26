## Description: <br>
Analyze GitHub Actions failures, summarize failed logs, identify likely root causes, and propose minimal fixes using the GitHub CLI and GitHub API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[martok9803](https://clawhub.ai/user/martok9803) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use CI Whisperer to investigate failing GitHub Actions runs, understand the failing job or step, and receive concise fix options. When explicitly approved and write mode is enabled, it can help prepare a minimal PR fix. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses the local GitHub CLI identity to inspect workflow runs and logs. <br>
Mitigation: Install only in environments where that local GitHub identity is appropriate for CI inspection, and authenticate with the GitHub CLI intentionally. <br>
Risk: CI logs can contain sensitive data. <br>
Mitigation: Review log excerpts before sharing or relying on them, and redact tokens, secrets, and other sensitive values. <br>
Risk: Optional PR fix mode can create branches or pull requests. <br>
Mitigation: Keep CI_WHISPERER_WRITE unset unless write behavior is desired, and require explicit user approval before creating a PR. <br>


## Reference(s): <br>
- [CI Whisperer configuration](references/config.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Guidance] <br>
**Output Format:** [Markdown report with command snippets, short redacted log excerpts, and optional patch or PR guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Default behavior is read-only; PR creation requires explicit user approval and CI_WHISPERER_WRITE=1.] <br>

## Skill Version(s): <br>
0.2.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
