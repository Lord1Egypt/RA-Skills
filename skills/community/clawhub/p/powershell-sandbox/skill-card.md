## Description:

Provides guidance and PowerShell command patterns for running scripts in a constrained sandbox with command filtering, timeout controls, output limits, file isolation, and pre-execution safety checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yuyonghao-123](https://clawhub.ai/user/yuyonghao-123)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and automation engineers use this skill to structure constrained PowerShell script execution with configurable timeouts, command allowlists, output limits, and working-directory controls. Server security evidence says the current artifact should be treated as documentation for a proposed tool until the implementation and controls are independently reviewed.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The artifact makes sandbox safety claims, but server security evidence says the package appears incomplete and should not be relied on for untrusted PowerShell execution.

Mitigation: Treat the release as documentation for a proposed tool until src/sandbox.ps1, tests, and security controls are present and independently reviewed.

Risk: The documented workflow includes options such as network access and configurable command allowlists that can increase exposure if enabled without review.

Mitigation: Keep network access disabled by default, use strict command allowlists, set short timeouts and output limits, and review scripts before execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yuyonghao-123/skills/powershell-sandbox)
- [Skill documentation](artifact/SKILL.md)
- [Test results](artifact/TEST_RESULTS.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with PowerShell command and code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Targets Windows PowerShell 5.1+ and PowerShell 7+ workflows with configurable timeout, output, network, working-directory, and command allowlist settings.]

## Skill Version(s):

0.1.0 (source: server release metadata, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
