## Description:

Post diary entries to a Nano diary platform via webhook, with support for creating entries and AI-powered merging with existing handwritten diaries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fengye607](https://clawhub.ai/user/fengye607)

### License/Terms of Use:


## Use Case:

External users and agents use this skill to submit plain-text diary entries for a specific date to a Nano diary account. It can create a new entry or update an existing same-date entry, including asynchronous AI merging when handwritten content already exists.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Diary content is private personal information sent to an external Nano diary service.

Mitigation: Use the skill only with a Nano account and endpoint the user trusts, and review diary content before sending it.

Risk: The reusable webhook token is placed in the request URL and may appear in shell history, process listings, or logs.

Mitigation: Store the token in NANO_DIARY_HOOK_TOKEN, avoid pasting real tokens into shared logs, and rotate the token if exposure is suspected.

Risk: Submitting an entry for a date that already exists may update, overwrite, or asynchronously merge existing diary content.

Mitigation: Confirm the target date and expected merge or update behavior before submitting same-date entries.

## Reference(s):

- [Nano Diary Hook on ClawHub](https://clawhub.ai/fengye607/skills/nano-diary-hook)
- [Nano diary webhook endpoint](https://image.yezishop.vip/api/diary-hook/${NANO_DIARY_HOOK_TOKEN})

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration]

**Output Format:** [Markdown with JSON and bash examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl and the NANO_DIARY_HOOK_TOKEN environment variable.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
