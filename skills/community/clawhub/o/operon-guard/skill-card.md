## Description:

Pre-flight trust verification for AI agents. Verify behavior, detect injection vulnerabilities, check for PII leaks, and measure reliability before granting Write/Execute permissions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[brainhiveinc](https://clawhub.ai/user/brainhiveinc)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to run pre-deployment behavioral checks on AI agents, including determinism, concurrency, safety, and latency tests before granting elevated tool permissions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The required operon-guard CLI is an unpinned external package.

Mitigation: Install it only from a trusted package source and prefer a pinned or reviewed version when available.

Risk: The documented scan, test, and init --agent flows import target Python code and can execute top-level code before checks run.

Mitigation: Review target source first and run checks in a sandbox when testing third-party or otherwise untrusted agents.

Risk: The quick scan command exits 0 even when it detects injection or PII issues.

Mitigation: Use operon-guard test for gating because it exits nonzero when the trust score fails.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/brainhiveinc/skills/operon-guard)
- [Publisher profile](https://clawhub.ai/user/brainhiveinc)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and YAML configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include guardfile YAML examples and command-line verification workflows.]

## Skill Version(s):

0.2.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
