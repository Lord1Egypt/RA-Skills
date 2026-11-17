## Description:

Uses the KANO framework from chapter 2 of AI超级个体 to classify product requirements as basic, performance, delighter, indifferent, or reverse, then generate an explainable priority order around baseline needs, incremental gains, and later surprises.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cglt2026opc](https://clawhub.ai/user/cglt2026opc)

### License/Terms of Use:

MIT-0

## Use Case:

Product managers, founders, and product teams use this skill to classify candidate requirements with a simplified KANO decision method and decide what to do now, next, later, or not at all. It supports prioritization discussions but does not replace user interviews, usability testing, or business constraints.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: KANO classifications may be mistaken for validated user research or a complete product decision.

Mitigation: Treat the output as decision support and validate uncertain or high-impact items with user interviews, usability testing, and business constraints before committing roadmap work.

Risk: The optional sorter runs a local Python script over user-provided JSON.

Mitigation: Review the input file and run the bundled script only in a trusted local workspace; the server security evidence reports no network access, credential handling, persistence, or destructive actions.

## Reference(s):

- [KANO 分类与排序](references/kano.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Guidance]

**Output Format:** [Markdown guidance with optional JSON input and JSON output from a local Python sorter]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces four priority buckets and short explanations; optional script sorts KANO-classified JSON items deterministically.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
