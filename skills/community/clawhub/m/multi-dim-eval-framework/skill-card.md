## Description:

Designs multi-dimensional evaluation frameworks for comparing AI systems across qualitative dimensions without collapsing results into a single score.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tatsuko-tsukimi](https://clawhub.ai/user/tatsuko-tsukimi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, evaluation leads, and AI system teams use this skill to design calibrated, group-wise scorecards for agents, RAG systems, deliberation systems, and other AI workflows where single metrics hide important tradeoffs. It helps define dimensions, canonical and proxy measurements, failure modes, and calibration cases before judging results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may provide sensitive logs, calibration cases, or system artifacts for the assistant to analyze while designing the evaluation framework.

Mitigation: Share only artifacts suitable for the assistant environment and redact confidential or regulated data before using the skill.

Risk: The artifact references templates/scorecard.md.tmpl, but the release evidence does not include that file.

Mitigation: Use the included examples and axes worksheet as scorecard guidance, and confirm any generated scorecard format before relying on it.

Risk: Proxy measurements and uncalibrated dimensions can produce misleading comparisons if treated as final benchmark results.

Mitigation: Run the framework on calibration cases, verify expected ordinals, and keep group-wise scores separate rather than creating a composite score.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tatsuko-tsukimi/skills/multi-dim-eval-framework)
- [README](README.md)
- [Group Design Principles](references/group-design-principles.md)
- [Canonical vs Proxy Decision](references/canonical-vs-proxy-decision.md)
- [MADEF Axes](references/madef-axes.md)
- [Memory Bench Taxonomy](references/memory-bench-taxonomy.md)
- [Axes Design Worksheet](templates/axes-design-worksheet.md)
- [Deliberation System Eval Example](examples/deliberation-system-eval.md)
- [Cross-Domain RAG Eval Example](examples/cross-domain-rag-eval.md)

## Skill Output:

**Output Type(s):** [guidance, markdown, configuration]

**Output Format:** [Markdown guidance, rubrics, worksheets, and scorecard structures]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces human-in-the-loop evaluation framework designs and group-wise scorecards; it does not run benchmarks or automated scoring.]

## Skill Version(s):

0.1.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
