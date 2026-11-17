## Description:

Provides command-line guidance for querying real-time Chilean public transport stop arrivals with human-readable or raw JSON output.

This skill is ready for commercial/non-commercial use.

## Publisher:

[iiroak](https://clawhub.ai/user/iiroak)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operators, and transit-data users can use this skill to install and run the iBus CLI for checking real-time bus arrivals at Chilean public transport stops. It supports service filtering, raw JSON output for pipelines, and documented exit-code behavior.

### Deployment Geography for Use:

Chile

## Known Risks and Mitigations:

Risk: The recommended installer runs a remote shell script from a mutable GitHub branch.

Mitigation: Prefer cloning the repository, inspecting the installer, and using the manual pip install path in an isolated environment; avoid running the one-line remote bash command with elevated privileges.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/iiroak/skills/ibuscl-cli)
- [iBus.CL API repository referenced by the skill](https://github.com/iiroak/iBus.CL-API)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration instructions, JSON, Markdown]

**Output Format:** [Markdown with inline shell commands and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Covers stop codes, optional service filtering, raw JSON output, Python module execution, response fields, time values, and exit codes.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
