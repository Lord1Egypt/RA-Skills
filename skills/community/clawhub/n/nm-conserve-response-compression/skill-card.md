## Description:

Compresses verbose responses by removing filler and framing to save 200-400 tokens.

This skill is ready for commercial/non-commercial use.

## Publisher:

[athola](https://clawhub.ai/user/athola)

### License/Terms of Use:

MIT-0

## Use Case:

Agent users apply the skill to make routine responses more concise while preserving useful context, technical precision, safety warnings, and uncertainty markers. It is intended for verbose responses where detail is not needed.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Removing hedging indiscriminately can make an uncertain answer sound more certain than its evidence supports.

Mitigation: Retain factual uncertainty markers when evidence is incomplete, and apply the compression advice only where it fits the response.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/athola/skills/nm-conserve-response-compression)
- [Project homepage (Clawdis metadata)](https://github.com/athola/claude-night-market/tree/master/plugins/conserve)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Concise natural-language text, optionally structured as Markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Targets 200-400 fewer tokens per response while maintaining clarity.]

## Skill Version(s):

1.10.4 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
