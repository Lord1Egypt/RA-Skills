## Description: <br>
Designs a multi-dimensional evaluation framework for AI systems where single-score benchmarks lose information. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tatsuko-tsukimi](https://clawhub.ai/user/tatsuko-tsukimi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, evaluators, and AI system teams use this skill to design calibrated, group-wise scorecards for comparing AI systems across qualitative dimensions when a single benchmark number would hide important tradeoffs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Evaluation logs, datasets, or internal records supplied during use may contain sensitive information. <br>
Mitigation: Only provide data that is allowed to be processed in the agent environment. <br>
Risk: Generated rubrics and scorecards may be incomplete or misleading if used without calibration. <br>
Mitigation: Review generated rubrics and calibrate them against known cases before relying on results for decisions. <br>


## Reference(s): <br>
- [Group Design Principles](references/group-design-principles.md) <br>
- [Canonical vs Proxy Decision](references/canonical-vs-proxy-decision.md) <br>
- [MADEF Axes](references/madef-axes.md) <br>
- [Memory Bench Taxonomy](references/memory-bench-taxonomy.md) <br>
- [Deliberation System Evaluation Example](examples/deliberation-system-eval.md) <br>
- [Cross-Domain RAG Evaluation Example](examples/cross-domain-rag-eval.md) <br>
- [Axes Design Worksheet](templates/axes-design-worksheet.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, configuration] <br>
**Output Format:** [Markdown guidance with structured worksheets, rubric definitions, and group-wise scorecard tables] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces methodology and scoring structure; it does not run benchmarks or automate scoring.] <br>

## Skill Version(s): <br>
0.1.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
