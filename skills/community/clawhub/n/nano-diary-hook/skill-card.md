## Description: <br>
Post diary entries to a Nano diary platform via webhook. Supports creating new entries and AI-powered merging with existing handwritten diaries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fengye607](https://clawhub.ai/user/fengye607) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users use this skill to submit plain-text diary entries for a specific date to their Nano account, including AI-generated reflections. It can create a new diary entry or update an existing entry through the documented webhook behavior. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Diary text and the webhook token are sent to the Nano diary endpoint. <br>
Mitigation: Install only when the endpoint is trusted, keep NANO_DIARY_HOOK_TOKEN secret, and avoid submitting content that should not leave the user's environment. <br>
Risk: Submitting the same date again may update or merge with an existing diary entry. <br>
Mitigation: Keep separate backups for diary records that should not be changed before resubmitting a date. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/fengye607/nano-diary-hook) <br>
- [Nano diary webhook endpoint](https://image.yezishop.vip/api/diary-hook/${NANO_DIARY_HOOK_TOKEN}) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, API Calls, Configuration] <br>
**Output Format:** [Markdown with JSON and bash examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl and NANO_DIARY_HOOK_TOKEN; sends date and plain-text diary content to the Nano diary webhook.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
