## Description:

Giraffe Guard scans OpenClaw skill directories for supply chain attack patterns, malicious code, and suspicious behavior using context-aware grep and Python AST analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lida408](https://clawhub.ai/user/lida408)

### License/Terms of Use:

Apache License 2.0

## Use Case:

Developers and security reviewers use this skill to scan OpenClaw skills and related repositories before installation or in CI, producing findings that help them review potential supply chain risks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads directories that users explicitly scan, including files that may contain secrets.

Mitigation: Run it only on intended paths and handle generated findings as potentially sensitive because they can include file paths and matched content.

Risk: SARIF output is not authoritative for CI gates until output encoding is fixed.

Mitigation: Treat SARIF results as advisory and require human review or additional validation before using them to block or approve releases.

Risk: Remote-looking targets such as git URLs, git@ addresses, or paths ending in .git can trigger a network clone during pre-install scanning.

Mitigation: Use local directories when network access is not intended, and pass remote targets only when cloning is expected.

Risk: The security verdict is suspicious, so a clean scanner result should not be the only release approval signal.

Mitigation: Pair scanner output with manual review and trusted provenance checks before deploying scanned skills.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lida408/skills/giraffe-guard)
- [OpenClaw project](https://github.com/openclaw/openclaw)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration, Guidance]

**Output Format:** [Terminal text, JSON reports, SARIF, and Markdown guidance with bash examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports severity thresholds, rule skipping, whitelist files, quiet mode, and exit codes for CI.]

## Skill Version(s):

3.1.0 (source: server release evidence and audit.sh VERSION)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
