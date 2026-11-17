## Description:

Probe memory/summary clarity via dual anchor questions: task progress, info gaps.

This skill is ready for commercial/non-commercial use.

## Publisher:

[athola](https://clawhub.ai/user/athola)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to check whether a saved memory or session summary clearly states completed work and bounded open questions before a handoff, checkpoint, or compression.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A qualitative clarity result can be mistaken for confirmation that a memory is factually correct.

Mitigation: Use the probe as a clarity check only; compare progress claims with task facts and read the underlying requirements before relying on the summary.

Risk: A model may sound confident despite an incomplete or inaccurate memory.

Mitigation: Use both progress and gap probes, and treat the result as a necessary quality check rather than a sufficient validation.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/athola/skills/nm-memory-palace-memory-clarity-probe)
- [Plugin homepage (metadata link)](https://github.com/athola/claude-night-market/tree/master/plugins/memory-palace)
- [Meta-Cognitive Memory Policy Optimization paper](https://arxiv.org/abs/2605.30159)

## Skill Output:

**Output Type(s):** [Markdown, Guidance]

**Output Format:** [Markdown clarity assessment with progress and gap probe scores, a composite result, a recommendation, and specific issues when needed]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Qualitative assessment of memory clarity; it does not verify factual correctness or compute token-level predictive entropy.]

## Skill Version(s):

1.10.3 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
