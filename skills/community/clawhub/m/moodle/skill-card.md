## Description:

Access a Moodle LMS via the REST API to check assignments, browse course content, and inspect completion status using curl.

This skill is ready for commercial/non-commercial use.

## Publisher:

[altusrossouw](https://clawhub.ai/user/altusrossouw)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users can use this skill to guide an agent in querying a configured Moodle instance for courses, assignments, course content, and completion status.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A Moodle API token can be sent to the hardcoded default server when MOODLE_URL is unset.

Mitigation: Set MOODLE_URL to the trusted Moodle server before use, keep MOODLE_TOKEN out of shared files and shell history, and rotate the token if it may have been sent to the default endpoint.

## Reference(s):

- [ClawHub Moodle skill page](https://clawhub.ai/altusrossouw/skills/moodle)
- [OpenClaw documentation](https://docs.openclaw.ai)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash, JSON, and Python snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl and a MOODLE_TOKEN; MOODLE_URL should be set to the user's trusted Moodle server.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
