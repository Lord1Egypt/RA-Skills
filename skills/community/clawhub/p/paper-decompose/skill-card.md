## Description:

Paper Decompose guides agents through a four-layer reading workflow for research papers and reports, extracting the core gap, delta, ASCII napkin sketch, and transferable inspirations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jack-long-2022](https://clawhub.ai/user/jack-long-2022)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and researchers use this skill to turn PDFs, arXiv links, URLs, or text from papers and research reports into a four-layer decomposition covering the core gap, delta, napkin sketch, and transferable inspirations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Investment-report outputs can include actions such as add, hold, reduce, or watch that may be mistaken for personalized financial advice.

Mitigation: Treat these outputs as research commentary and make financial decisions only after independent review or consultation with a qualified advisor.

Risk: The skill analyzes user-provided documents and can produce misleading conclusions if the input is incomplete, unparseable, or outside the stated document scope.

Mitigation: Confirm the source document is parseable and within the skill limits before relying on the decomposition.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jack-long-2022/skills/paper-decompose)
- [Process guide](artifact/PROCESS.md)
- [Output template](artifact/TEMPLATE.md)
- [Sample report test case](artifact/test-cases/sample-report.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown structured as a four-layer analysis with optional ASCII diagrams and investment impact assessment]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a parseable document and is scoped away from documents over 200 pages, purely theoretical work, marketing-only reports, and previously-read papers.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
