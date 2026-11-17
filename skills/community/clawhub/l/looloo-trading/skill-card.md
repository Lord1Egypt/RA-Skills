## Description:

Use this skill when the user wants a LooLoo trade quote or a website confirmation link for a buy or sell.

This skill is ready for commercial/non-commercial use.

## Publisher:

[looloolol](https://clawhub.ai/user/looloolol)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to get LooLoo buy or sell quotes and, after explicit confirmation, receive a website confirmation link for final wallet signing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A user could act on an unexpected token, side, size, or destination domain in a generated trade confirmation flow.

Mitigation: Review the quote details before continuing and only sign wallet transactions on the LooLoo website when the token, side, amount, and destination domain match the user's intent.

Risk: A trade intent could be created before the user has explicitly agreed to continue.

Mitigation: Create a trade intent only after presenting the quote summary and receiving explicit user confirmation.

## Reference(s):

- [LooLoo Trading on ClawHub](https://clawhub.ai/looloolol/skills/looloo-trading)

## Skill Output:

**Output Type(s):** [text, markdown, API Calls, guidance]

**Output Format:** [Markdown with quote summaries and confirmation links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires explicit user confirmation before creating a trade intent; final wallet signing happens on the LooLoo website.]

## Skill Version(s):

0.1.2 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
