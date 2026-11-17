## Description:

SmartHR (smarthr.jp). Use this skill for ANY SmartHR request — reading, creating, updating, and deleting data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

HR teams and administrators can use an agent to read and manage employee records, departments, job classifications, and related SmartHR data, and to invite employees. The skill describes approval steps for changes and deletions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The automatic CLI setup can execute remote code, and the installer contents were unavailable for review.

Mitigation: Review and verify the installer and release before setup, and check or disable automatic installation of other agent skills.

Risk: SmartHR access can expose HR data or allow changes and deletions to employee records.

Mitigation: Connect only the necessary SmartHR permissions, understand OOMOL's role in handling HR data, and retain approval for every write or deletion.

## Reference(s):

- [SmartHR](https://smarthr.jp/)
- [SmartHR API documentation](https://developer.smarthr.jp/api)
- [oo CLI repository](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [Shell commands, JSON, Guidance]

**Output Format:** [oo CLI commands with JSON action payloads and JSON responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Covers read, write, and destructive SmartHR actions.]

## Skill Version(s):

1.0.2 (source: frontmatter, server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
