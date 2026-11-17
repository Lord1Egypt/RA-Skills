## Description:

Detects whether AI responses may contain hallucinations by analyzing tool usage, response quality, and handling of invalid premises.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jdchi](https://clawhub.ai/user/jdchi)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to have an agent review responses for possible hallucinations, missing verification, and correct handling of invalid premises. It can run on explicit fact-check requests or, when enabled, after every response.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may review and summarize prior conversation turns, which can expose private or confidential content.

Mitigation: Keep it disabled unless explicitly needed, and avoid using it in conversations containing private, confidential, or regulated information.

Risk: Automatic fact-check output can disrupt workflows that require strict machine-readable responses.

Mitigation: Disable the skill for strict JSON, API-style, or other machine-readable output workflows.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/jdchi/skills/is-bullshit)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown fact-check summaries in the user's language]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Shows all rounds for conversations of five or fewer rounds; for longer conversations, shows only suspicious rounds.]

## Skill Version(s):

1.7.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
