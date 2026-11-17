## Description:

Convenes independent AI advisors to deliberate on high-stakes, ambiguous, or contested questions, then synthesizes disagreement into a final answer.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ddanninger](https://clawhub.ai/user/ddanninger)

### License/Terms of Use:

MIT-0

## Use Case:

Employees, external users, and developers use this skill to get structured second opinions on decisions where a single response may miss dissent, hidden assumptions, or stakeholder impacts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad trigger phrases can activate the council for simple questions, adding unnecessary cost and latency.

Mitigation: Use the skill when the user explicitly wants multiple perspectives or the decision is high-stakes, ambiguous, or contested; avoid it for simple factual lookups or mechanical tasks.

Risk: Decision-critical guidance may still be incomplete or wrong, even after multi-perspective review.

Mitigation: Verify important claims and use the final falsifier and flip conditions before acting on consequential recommendations.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ddanninger/skills/llm-council)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown synthesis with verdict, vote tally, consensus, dissent, flip conditions, and a concrete falsifier.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May add cost and latency because the workflow can launch several subagents and may use search or code inspection when available.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
