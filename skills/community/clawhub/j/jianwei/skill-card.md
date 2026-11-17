## Description:

Jianwei is a Chinese-language dual-engine strategic analysis skill that generates hypotheses, performs directed verification, and produces evidence-backed strategic recommendations for market, competition, transformation, portfolio, growth, and organization questions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tuobadaidai](https://clawhub.ai/user/tuobadaidai)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and strategy teams use this skill to structure strategic decisions, industry research, market-entry assessments, competitive analysis, transformation choices, business model analysis, growth strategy, organization diagnosis, and strategic reports. It is not intended for pure data lookup, financial modeling, operational optimization, PRDs, or technical architecture design.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Strategic recommendations may be wrong or under-evidenced if user inputs, market data, competitor signals, or cited sources are incomplete.

Mitigation: Review core assumptions, cited evidence, confidence labels, and exit criteria before acting on recommendations, especially for high-impact business decisions.

Risk: The skill may suggest using search or optional expert skills for evidence checking, which can affect completeness depending on tool availability.

Mitigation: Confirm which tools and expert skills were actually available during the run and clearly label any analysis completed without external verification or independent review.

## Reference(s):

- [Jianwei Skill Page](https://clawhub.ai/tuobadaidai/skills/jianwei)
- [Publisher Profile](https://clawhub.ai/user/tuobadaidai)
- [Hypothesis Generation and Screening](references/engine-judgment/hypothesis-generation.md)
- [Insight Generation Mechanisms](references/engine-judgment/insight-generation.md)
- [Directed Verification](references/engine-verification/directed-verification.md)
- [Premise Check](references/engine-judgment/premise-check.md)
- [Diagnosis and Guidance](references/engine-judgment/diagnosis-guidance.md)
- [Cost Quantification](references/engine-verification/cost-quantification.md)
- [Coherent Actions](references/engine-judgment/coherent-actions.md)
- [Red Team Protocol](references/engine-judgment/red-team.md)
- [Constitutional Audit and Citation Check](references/engine-verification/constitutional-audit.md)
- [Complexity Routing](references/shared/complexity-routing.md)
- [Output Specification](references/shared/output-spec.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown strategic analysis report with executive summary, strategic map, evidence chain, feasibility analysis, coherent actions, verification notes, red-team review, and audit notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include Mermaid diagrams, confidence labels, source notes, cost estimates, implementation milestones, and exit criteria when the analysis path calls for them.]

## Skill Version(s):

1.1.0 (source: release evidence and frontmatter metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
