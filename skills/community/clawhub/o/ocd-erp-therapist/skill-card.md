## Description:

Guides structured self-directed OCD exposure and response prevention practice using inhibitory learning, safety screening, progress tracking, reminders, and tailored exposure support.

This skill is ready for commercial/non-commercial use.

## Publisher:

[arclunar](https://clawhub.ai/user/arclunar)

### License/Terms of Use:


## Use Case:

External users use this skill as a self-directed ERP coaching aid for OCD practice, including safety screening, exposure planning, timed check-ins, progress review, and relapse prevention. It is intended as support and psychoeducation, not a replacement for professional mental-health care.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Scheduled reminders and Feishu notifications can create unwanted automation or disclose sensitive ERP activity.

Mitigation: Review all reminder commands before enabling them, keep recipients limited, and remove cron jobs by exact ID when sessions end.

Risk: ERP session records and progress logs may contain sensitive mental-health information saved locally.

Mitigation: Save records only with user consent, keep files in protected local storage, and avoid sharing logs through notification channels.

Risk: Generated report text and bulk cleanup pipelines can lead to unsafe shell command construction.

Mitigation: Use structured file-writing APIs for generated content and avoid broad shell pipelines; prefer exact command arguments and exact cron IDs.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/arclunar/skills/ocd-erp-therapist)
- [International OCD Foundation Find Help](https://iocdf.org/find-help/)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration]

**Output Format:** [Conversational guidance with markdown checklists, session notes, and optional shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce ERP session records, progress summaries, reminder commands, and safety-oriented recommendations.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
