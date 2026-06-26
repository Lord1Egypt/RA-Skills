## Description: <br>
Sync and summarize student Moodle data including courses, upcoming deadlines, grades, files, and announcements. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yerassyl-sailaubay](https://clawhub.ai/user/yerassyl-sailaubay) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Students and education-focused agents use this skill to retrieve Moodle course data, deadlines, grades, notifications, and course resources, then turn them into snapshots, reports, digests, and study plans. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses MOODLE_TOKEN to access student Moodle data, including courses, grades, deadlines, files, and notifications. <br>
Mitigation: Install only when Moodle account access is intended, use the least-privilege Moodle token available, and keep MOODLE_TOKEN out of shared logs and screenshots. <br>
Risk: Generated snapshots and reports can contain private academic records when written to files or shared from stdout. <br>
Mitigation: Prefer HTTPS for MOODLE_URL and store exported reports in a private location with appropriate access controls. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/yerassyl-sailaubay/moodle-student-sync) <br>
- [Publisher profile](https://clawhub.ai/user/yerassyl-sailaubay) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [JSON snapshots and Markdown reports, digests, and study plans] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3, requests, MOODLE_URL, and MOODLE_TOKEN; MOODLE_USER_ID is optional.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release metadata and artifact/skill.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
