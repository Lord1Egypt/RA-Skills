## Description:

MaiMemo Open API skill for vocabulary learning, including vocabulary lookup, custom definitions, mnemonics, word lists, example sentences, study progress, review schedules, and study records.

This skill is ready for commercial/non-commercial use.

## Publisher:

[celend](https://clawhub.ai/user/celend)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to help an authenticated MaiMemo account query vocabulary data, manage learner-created definitions, mnemonics, word lists, and example sentences, and inspect or update study progress and review schedules.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A live MAIMEMO_TOKEN can grant access to authenticated MaiMemo study records and account-changing actions.

Mitigation: Configure MAIMEMO_TOKEN through a secure environment or secret manager, avoid pasting it into chat, and rotate the token if it has been shared.

Risk: The skill can read, export, modify, and delete authenticated study data, including adding words and advancing review schedules.

Mitigation: Review proposed API calls before execution and use the skill only when account-level data access and changes are intended.

Risk: Study endpoints are marked beta and may be unavailable or inaccurate without MaiMemo automatic sync and same-day app initialization.

Mitigation: Treat study progress and schedule results as operational data that may need confirmation in MaiMemo before relying on them.

## Reference(s):

- [Memo Api skill page](https://clawhub.ai/celend/skills/memo-api)
- [MaiMemo Open API base](https://open.maimemo.com/open/api/v1)
- [MaiMemo Open API token page](https://open.maimemo.com/open/api/v1/tokens/openapi)
- [Vocabulary API](references/vocabulary-api.md)
- [Interpretations API](references/interpretations-api.md)
- [Notes API](references/notes-api.md)
- [Notepads API](references/notepads-api.md)
- [Phrases API](references/phrases-api.md)
- [Study API](references/study-api.md)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, API calls, Configuration]

**Output Format:** [Markdown with curl examples and JSON request or response snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires MAIMEMO_TOKEN and curl; API calls operate on the authenticated MaiMemo account.]

## Skill Version(s):

1.2.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
