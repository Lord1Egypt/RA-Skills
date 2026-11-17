## Description:

Simple local security check (firewall, updates, ssh status) without external dependencies.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fedrov2025](https://clawhub.ai/user/fedrov2025)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and system operators use this skill to run a small local health check on macOS or Linux hosts and capture firewall, open-port, software-update, and SSH daemon status in a report.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may prompt for sudo while checking firewall status, open ports, and available updates.

Mitigation: Review check.sh before use, run it from a trusted directory, and approve only the expected local inspection commands.

Risk: The generated report records host-security details such as firewall, listening-port, update, and SSH status in a predictable local file.

Mitigation: Keep the report in a controlled workspace, restrict access to it, and avoid sharing it publicly.

Risk: Running the entire script as root would broaden the impact of any local path or report-file issue.

Mitigation: Run the skill as a normal user and allow sudo only for individual commands when prompted.

## Reference(s):


## Skill Output:

**Output Type(s):** [markdown, shell commands, guidance]

**Output Format:** [Markdown report with local command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes a dated report to memory/healthcheck-YYYY-MM-DD.md and may prompt for sudo during local inspection commands.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
