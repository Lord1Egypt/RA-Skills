## Description:

Integrates with Moodle 4.x REST Web Services to help agents create courses, manage enrollments, update activities, send grades, and list courses or students.

This skill is ready for commercial/non-commercial use.

## Publisher:

[exeandino](https://clawhub.ai/user/exeandino)

### License/Terms of Use:


## Use Case:

Developers, educators, and administrators use this skill to automate Moodle 4.x course, enrollment, activity, grading, and roster workflows through REST Web Services.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Moodle Web Service tokens can expose administrative access if pasted into chat, committed to version control, or reused broadly.

Mitigation: Store tokens only in local unversioned configuration or environment-specific secret storage, and use least-privilege Moodle tokens for the requested tasks.

Risk: Course, enrollment, activity, or grade changes can affect live Moodle users if executed against production without review.

Mitigation: Test changes in a staging course first and require clear user confirmation before modifying grades, enrollments, courses, or activities.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/exeandino/skills/moodle-ws-skill)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with code, shell command, and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include Moodle REST request guidance and local secret configuration recommendations.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
