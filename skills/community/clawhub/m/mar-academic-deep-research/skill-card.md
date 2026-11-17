## Description:

Academic Deep Research guides agents through scoped, user-approved research plans, two-cycle investigation per theme, source-quality checks, APA-style citations, and narrative synthesis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[marjoriebroad](https://clawhub.ai/user/marjoriebroad)

### License/Terms of Use:

MIT-0

## Use Case:

External users, researchers, analysts, and developers use this skill when they need transparent deep research, literature reviews, competitive intelligence, or multi-source claim verification with visible methodology and citations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad automated web research and parallel sub-agents may gather irrelevant, low-quality, or sensitive context if the topic is not scoped clearly.

Mitigation: Require the documented clarification and plan-approval checkpoints before research execution, including source preferences, time bounds, geography, and exclusions.

Risk: Persistent memory access may reuse prior-session content that the user did not intend to include.

Mitigation: Use memory-free mode by default and only query memory after explicit user approval for the specific research task.

Risk: Final research reports can still contain unresolved contradictions, dated sources, or low-confidence claims.

Mitigation: Preserve confidence labels, contradiction notes, source-quality assessments, and limitations, and verify high-impact claims against primary sources before acting on them.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/marjoriebroad/skills/mar-academic-deep-research)
- [Publisher Profile](https://clawhub.ai/user/marjoriebroad)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown research plans, progress analysis, citations, and final narrative reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include confidence labels, APA-style references, source-quality discussion, contradiction analysis, and documented limitations.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
