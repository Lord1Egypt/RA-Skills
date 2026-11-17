## Description:

Integrates with Moodle 4.x Web Services REST to create and duplicate courses, manage enrollments, create activities, update grades, list courses and students, and send internal messages.

This skill is ready for commercial/non-commercial use.

## Publisher:

[exeandino](https://clawhub.ai/user/exeandino)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and LMS administrators use this skill to automate Moodle course setup, enrollment changes, activity creation, grade updates, student listing, and internal messaging through Moodle REST APIs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires a Moodle web-service token that may carry meaningful LMS authority.

Mitigation: Use a least-privilege token, store it outside Git, never expose it in chat, and regenerate it if it is exposed.

Risk: Maintenance scripts can delete courses or categories based on generated target lists.

Mitigation: Independently review the target list, verify the configured Moodle URL, and confirm backups before running deletion scripts.

Risk: Bulk messaging and course or category changes can execute immediately when invoked.

Mitigation: Review message text, course IDs, category IDs, and recipient scope before execution.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with command arguments and Moodle action summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May execute Moodle REST actions through local Python scripts when a configured Moodle URL and token are available.]

## Skill Version(s):

1.3.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
