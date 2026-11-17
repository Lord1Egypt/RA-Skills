## Description:

Uploads IELTS reading review JSON files to a remote dashboard so learners can review their history and progress trends.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dengjiawei1226](https://clawhub.ai/user/dengjiawei1226)

### License/Terms of Use:

MIT-0

## Use Case:

External learners and tutoring workflows use this skill to upload existing IELTS reading review data and receive a dashboard link for reviewing records and progress trends.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The upload workflow sends review data and optional HTML content to tuyaya.online.

Mitigation: Review the destination and data contents before running the upload, and avoid optional HTML uploads unless sharing the full file contents is acceptable.

Risk: The script can derive a stable identifier from the machine hostname and local username.

Mitigation: Set explicit IELTS_USER_ID and IELTS_USER_NAME values before running the script.

Risk: A shared API key may appear in generated links or logs.

Mitigation: Treat generated dashboard links as sensitive and avoid sharing logs that include the key.

Risk: The skill text describes a remote script fallback.

Mitigation: Use the bundled local script after review instead of downloading a remote replacement at runtime.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dengjiawei1226/skills/ielts-review-upload)
- [Online reading review dashboard](https://tuyaya.online/ielts/reading.html)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands and dashboard URLs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May print user-specific dashboard links and upload status from the shell script.]

## Skill Version(s):

2.1.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
