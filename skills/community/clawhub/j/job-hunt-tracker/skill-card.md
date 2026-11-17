## Description:

Job Hunt Tracker helps an agent log and manage job applications, interviews, offers, follow-ups, reports, and job-search statistics using local files.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mkpareek0315](https://clawhub.ai/user/mkpareek0315)

### License/Terms of Use:


## Use Case:

External users use this skill to keep a local job-search record, update application statuses, prepare for interviews, compare offers, and generate follow-up text and progress summaries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores job-search details such as salary, offers, notes, and rejection history on the user's machine.

Mitigation: Avoid entering sensitive details that should not be stored locally, and review or delete ~/.openclaw/job-hunt-tracker/ when the tracker is no longer needed.

Risk: Salary guidance, application suggestions, and interview preparation content can be approximate or outdated.

Mitigation: Treat generated guidance as planning support and verify important compensation, company, and role information with current authoritative sources before acting.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mkpareek0315/skills/job-hunt-tracker)
- [ClawHub publisher profile](https://clawhub.ai/user/mkpareek0315)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown responses with JSON and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates and updates local JSON files under ~/.openclaw/job-hunt-tracker/ when the hosting agent grants read/write access.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
