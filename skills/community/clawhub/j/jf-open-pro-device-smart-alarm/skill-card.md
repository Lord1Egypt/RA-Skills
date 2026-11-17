## Description:

Manages JFTech device smart alarm capabilities, including device ability checks, motion alarm switches, alarm schedules, alarm message lists, and alarm image retrieval.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jftech](https://clawhub.ai/user/jftech)

### License/Terms of Use:

MIT-0

## Use Case:

Device operators and integrators use this skill to inspect and update smart-alarm settings for bound JFTech devices, query alarm history, and retrieve short-lived alarm image URLs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can send device credentials, tokens, configuration data, and alarm image metadata to an endpoint selected by environment variable.

Mitigation: Use only the documented jftechws.com regional hosts for JF_ENDPOINT and review environment variables before execution.

Risk: Actions that disable alarms, notifications, or schedules change live device monitoring.

Mitigation: Require operator confirmation for alarm-disabling changes and verify the resulting device configuration after updates.

Risk: Alarm lists and picture URLs may expose sensitive surveillance data.

Mitigation: Limit access to authorized users, avoid logging or sharing picture URLs unnecessarily, and handle returned URLs as sensitive data.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jftech/skills/jf-open-pro-device-smart-alarm)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and JSON-style command results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include live device configuration changes, alarm metadata, and alarm image URLs.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact frontmatter reports 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
