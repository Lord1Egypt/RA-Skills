## Description:

Academic Deep Research guides an agent through scoped, multi-cycle web research with visible methodology, source-confidence checks, APA-style citations, and human checkpoints before producing a research report.

This skill is ready for commercial/non-commercial use.

## Publisher:

[marjoriebroad](https://clawhub.ai/user/marjoriebroad)

### License/Terms of Use:

MIT-0

## Use Case:

External users, researchers, analysts, and developers use this skill to plan and conduct rigorous deep research, literature reviews, competitive intelligence, and multi-source verification where methodology and limitations need to be visible.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can send research topics and source requests through web search and page-fetching tools.

Mitigation: Use it only for topics approved for network research, and avoid confidential, regulated, or proprietary queries unless the agent environment permits external lookup.

Risk: The skill asks the agent to consult persistent memory, but the appropriate memory scope may not be clear.

Mitigation: Disable or limit persistent memory access unless the available memory is known to contain only relevant and permitted prior work.

Risk: The final report may sound authoritative even when sources conflict or evidence is weak.

Mitigation: Require human review of cited sources, confidence annotations, unresolved contradictions, and limitations before relying on conclusions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/marjoriebroad/skills/marjorie-academic-deep-research)
- [Artifact README](artifact/README.md)
- [Artifact quick reference](artifact/quickref.md)
- [Artifact example workflow](artifact/example.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown research plans and narrative reports with APA-style citations and source-confidence notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include clarifying questions, research plans, tool-use rationale, confidence annotations, limitations, and final report sections.]

## Skill Version(s):

1.0.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
