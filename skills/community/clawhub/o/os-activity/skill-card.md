## Description:

Personalize OpenClaw by learning your operating system activity.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xiaobao520123](https://clawhub.ai/user/xiaobao520123)

### License/Terms of Use:

MIT

## Use Case:

OpenClaw users and agents use this skill to inspect recent files, recently accessed directories, installed programs, and running processes so responses can be personalized to local OS activity.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can expose detailed local activity metadata, including file paths, directory history, installed applications, and full running-process command lines.

Mitigation: Use it only where that data is appropriate to inspect, and add consent, scoping, and redaction before use around credentials, customer data, private projects, or regulated information.

## Reference(s):

- [OS Activity ClawHub Skill Page](https://clawhub.ai/xiaobao520123/skills/os-activity)
- [osquery Releases](https://github.com/osquery/osquery/releases/)
- [README.md](README.md)
- [SKILL.md](SKILL.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown guidance with inline shell commands and pipe-delimited text tables]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Python and an osquery binary; available queries vary by operating system.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
