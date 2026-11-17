## Description:

OpenClaw Security Vulnerability Monitor - Checks for OpenClaw security vulnerabilities from NVD CVE database and GitHub Security Advisories.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aaronjager92](https://clawhub.ai/user/aaronjager92)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw operators use this skill to check the local OpenClaw version against NVD CVE records and GitHub Security Advisories, with vulnerability reports and remediation guidance when findings are detected.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup script installs an enabled recurring OpenClaw scheduled task.

Mitigation: Review or disable setup_cron.sh before installation, and use an opt-in schedule with clear uninstall steps.

Risk: The setup script accepts a delivery channel argument with unsafe input handling.

Mitigation: Avoid untrusted delivery channel values and review any customized delivery configuration before enabling the job.

Risk: The monitor depends on unpinned Python packages and external advisory APIs.

Mitigation: Pin dependency versions and account for NVD or GitHub API availability before relying on the monitor operationally.

## Reference(s):

- [NVD CVE API](https://services.nvd.nist.gov/rest/json/cves/2.0)
- [GitHub Security Advisories API](https://api.github.com/advisories)
- [Python requirements](references/requirements.txt)
- [ClawHub skill page](https://clawhub.ai/aaronjager92/skills/openclaw-self-guard)
- [Publisher profile](https://clawhub.ai/user/aaronjager92)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown vulnerability report or JSON status output, with setup guidance and shell command usage]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Runs silently when no vulnerabilities are found unless JSON output is requested.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
