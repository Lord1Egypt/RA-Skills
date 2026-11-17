## Description:

Helps an agent write responses, explanations, stories, instructions, and prose in iambic pentameter while preserving accuracy, clarity, and meaning.

This skill is ready for commercial/non-commercial use.

## Publisher:

[adamkessler](https://clawhub.ai/user/adamkessler)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill when they want an agent to answer in a Shakespearean or metered poetic style. It is suited to creative, explanatory, instructional, and conversational prose, while keeping structured technical outputs unmetered.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Verse constraints can reduce precision or clarity in safety-critical, legal, medical, financial, or precision technical answers.

Mitigation: Ask the agent to prioritize plain accuracy over verse for high-stakes or precision-sensitive tasks.

Risk: Forcing meter can alter structured outputs such as code, JSON, file paths, or shell commands.

Mitigation: Keep technical blocks unmetered and use metered framing only, as the skill directs.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/adamkessler/skills/iambic-pentameter)

## Skill Output:

**Output Type(s):** [text, markdown, code, guidance]

**Output Format:** [Markdown or plain text with metered verse lines; fenced technical blocks remain unmetered when needed.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Blank verse is preferred; rhyme is optional and should not be forced.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
