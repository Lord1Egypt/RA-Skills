## Description:

Issuefinder Tool helps agents download vehicle logs, process local log archives, and request IssueFinder fault analysis by VIN and event time.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lichm1007](https://clawhub.ai/user/lichm1007)

### License/Terms of Use:


## Use Case:

Developers and vehicle log analysts use this skill to run IssueFinder CLI workflows for cloud log download, local archive extraction and parsing, and reboot or fault analysis from VIN and event-time inputs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The tool may automatically replace itself with unverified server-provided code and continue executing a home-directory copy.

Mitigation: Run only trusted releases and servers, use --skip-version-check where appropriate until updater verification is fixed, and review any cached home-directory script before execution.

Risk: Vehicle logs, VINs, and timestamps may be sent to the configured IssueFinder service.

Mitigation: Use the skill only where sharing that data with the configured service is approved, prefer the trusted HTTPS server, and avoid custom or HTTP servers.

Risk: Archives and downloaded outputs may contain untrusted content.

Mitigation: Process files in an isolated workspace, scan outputs before opening or reusing them, and clean up retained logs according to local data-handling policy.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lichm1007/skills/issuefinder-tool)
- [IssueFinder server endpoint](https://issuefinder-playground-init-dev.inner.chj.cloud)
- [Wrapper usage documentation](artifact/WRAPPER_USAGE.md)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, Files, Analysis]

**Output Format:** [Markdown guidance with command examples; CLI runs print text summaries and save downloaded or parsed log files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs can include vehicle log files, extracted archive contents, parsed logs, reboot reason, final analysis result, screen status, task IDs, environment IDs, and output paths.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata; artifact CLI reports 1.1.3)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
