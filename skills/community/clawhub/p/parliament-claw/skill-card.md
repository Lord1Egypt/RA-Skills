## Description:

Play The Parliament Game to label Canadian parliamentary Q&A pairs and help evaluate whether MPs answered the questions they were asked.

This skill is ready for commercial/non-commercial use.

## Publisher:

[idiom-bytes](https://clawhub.ai/user/idiom-bytes)

### License/Terms of Use:

MIT-0

## Use Case:

External users and civic-tech participants use this skill to review Canadian House of Commons Q&A pairs, decide whether answers are substantive or non-responses, and submit confirmed labels for a civic accountability dataset.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill contacts qa.canada-central.com, auto-registers on first use, and stores or uses a labeling token.

Mitigation: Review the first-use registration behavior and use a dedicated PARLIAMENT_GAME_TOKEN when clearer credential control is needed.

Risk: The skill sends the agent or model name and submits user-approved labels to the external service.

Mitigation: Show each Q&A pair to the user, obtain explicit confirmation or override, and submit only labels the user approves.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/idiom-bytes/skills/parliament-claw)
- [The Parliament Game website](https://qa.canada-central.com)
- [The Parliament Game API documentation](https://qa.canada-central.com/docs)
- [Canada Central parent project](https://canada-central.com)
- [Source repository](https://github.com/idiom-bytes/parliament_qa_labelling)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands, configuration]

**Output Format:** [Markdown guidance with HTTP request examples and label summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires user confirmation before submitting labels; may use PARLIAMENT_GAME_TOKEN for credential control.]

## Skill Version(s):

2.1.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
