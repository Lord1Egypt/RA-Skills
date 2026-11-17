## Description:

Turns brainstorm-worthy voice or keyboard transcripts into pending to-do cards with prompts for a guided brainstorming session in Claude.

This skill is ready for commercial/non-commercial use.

## Publisher:

[samuel-wei](https://clawhub.ai/user/samuel-wei)

### License/Terms of Use:

MIT-0

## Use Case:

HiJavis users can turn recent voice notes or keyboard input into a pending calendar card and a ready-to-paste prompt for brainstorming in Claude. The skill can run automatically after each completed input or on request, using the last 24 hours of transcripts by default for manual requests.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automatic processing can examine sensitive voice and keyboard transcripts before a user confirms a card; manual use reads the last 24 hours by default.

Mitigation: Enable only if transcript processing is acceptable; review pending cards and prompts before confirming or using them, and disable the skill if automatic transcript-derived cards or chat digests are unwanted.

## Reference(s):

- [Brainstorming release on ClawHub](https://clawhub.ai/samuel-wei/skills/javis-brainstorming)
- [To-do card contract](references/todo-card-contract.md)
- [HiJavis iPhone app](https://apps.apple.com/us/app/hijavis/id6745134765)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Pending to-do card with a ready-to-paste prompt and a Markdown chat digest]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Cards require confirmation or discard; the skill does not perform the brainstorming itself.]

## Skill Version(s):

0.6.4 (source: server-resolved release, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
