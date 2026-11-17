## Description:

Analyze GitHub Actions failures and propose fixes using the GitHub CLI and GitHub API to fetch run metadata and logs, then produce a concise root-cause and next-steps report.

This skill is ready for commercial/non-commercial use.

## Publisher:

[martok9803](https://clawhub.ai/user/martok9803)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to triage failing GitHub Actions runs, summarize failed logs, identify likely root causes, and choose minimal fixes. It can also guide an opt-in PR fix workflow when explicitly requested and locally enabled.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The helper can print raw GitHub Actions failure logs from authenticated repositories, which may contain sensitive information.

Mitigation: Review and redact log excerpts before sharing them outside the trusted session.

Risk: PR creation can modify repositories if write mode is enabled and the user explicitly requests a fix.

Mitigation: Keep the default read-only mode unless PR creation is intended, and set CI_WHISPERER_WRITE=1 only for sessions where that behavior is acceptable.

Risk: The skill depends on an authenticated GitHub CLI session to read Actions runs and logs.

Mitigation: Install only where use of authenticated GitHub CLI access for the target repositories is acceptable.

## Reference(s):

- [CI Whisperer configuration](references/config.md)
- [ClawHub skill page](https://clawhub.ai/martok9803/skills/martok9803-ci-whisperer)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown report with shell commands and optional patch or PR guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include short redacted CI log excerpts, ranked likely causes, minimal fix options, and confidence level.]

## Skill Version(s):

0.2.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
