## Description:

Probe memory/summary clarity via dual anchor questions: task progress, info gaps

This skill is ready for commercial/non-commercial use.

## Publisher:

[athola](https://clawhub.ai/user/athola)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to assess whether a memory, summary, or session state clearly records completed work and bounded information gaps before handoff, checkpointing, or completion.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Qualitative probing can encourage premature confidence and does not validate whether remembered task facts are true.

Mitigation: Use the probe as a clarity check, then compare progress claims with task requirements and known facts before relying on the memory.

## Reference(s):

- [Memory Palace plugin](https://github.com/athola/claude-night-market/tree/master/plugins/memory-palace)
- [ClawHub release page](https://clawhub.ai/athola/skills/nm-memory-palace-memory-clarity-probe)
- [MMPO paper](https://arxiv.org/abs/2605.30159)

## Skill Output:

**Output Type(s):** [Analysis, Guidance, Text]

**Output Format:** [Markdown clarity assessment with progress and gap probe scores, a composite score, recommendation, and specific issues when needed]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Qualitative assessment; it does not calculate token-level predictive entropy or establish factual correctness.]

## Skill Version(s):

1.10.4 (source: server-resolved ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
