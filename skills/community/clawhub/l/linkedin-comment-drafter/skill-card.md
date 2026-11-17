## Description:

Draft a LinkedIn comment on someone else's post from its URL, producing 1-3 user-voice variants with a suggested reaction and approval step before posting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sergebulaev](https://clawhub.ai/user/sergebulaev)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to draft top-level LinkedIn comments from post URLs, compare a few concise variants, and approve a selected comment before publishing. It is not intended for replying to existing comments.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill includes guidance that can make automated LinkedIn engagement look human.

Mitigation: Require explicit user review and approval before posting, and remove or ignore timing guidance unless it complies with LinkedIn rules and the user's transparency standards.

Risk: The skill includes sales-prospecting cadence guidance for commenting on target-account posts.

Mitigation: Use the skill only for user-approved comments that comply with platform rules and organizational engagement standards; avoid prospecting cadence guidance unless explicitly permitted.

## Reference(s):

- [Comment Templates](references/comment-templates.md)
- [Examples](references/examples.md)
- [Voice Rules](references/voice-rules.md)

## Skill Output:

**Output Type(s):** [text, markdown, API calls, guidance]

**Output Format:** [Markdown with draft comment variants, reaction suggestions, template labels, engagement rationale, and an approval prompt]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Draft comments are constrained to 200-350 characters and 1-2 short paragraphs, with no hashtags and no em dashes.]

## Skill Version(s):

1.0.9 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
