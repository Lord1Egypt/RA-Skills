## Description: <br>
Paper Decompose helps agents produce four-layer deep readings of research papers and reports, covering the gap, delta, napkin sketch, and transferable insights. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jack-long-2022](https://clawhub.ai/user/jack-long-2022) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, researchers, analysts, and external users use this skill to turn PDFs, arXiv links, URLs, or text into a structured review of a paper, research report, article, or white paper. It is designed for deep reading workflows that need a problem gap, core contribution, before-and-after ASCII sketch, and cross-domain implications rather than a plain summary. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Investment-impact labels and position suggestions may be mistaken for personalized financial advice or current market research. <br>
Mitigation: Treat investment sections as non-personal analysis, verify claims against current market data, and review decisions with appropriate financial expertise. <br>
Risk: A structured four-layer output may overstate the novelty or reliability of weak source material. <br>
Mitigation: Check the original paper or report, especially the evidence for the stated gap, core delta, and comparison metrics. <br>
Risk: The skill is designed for documents with analyzable research or report structure and may fit poorly on very long reviews, pure theory, or marketing material. <br>
Mitigation: Use the documented input checks and fall back to another review workflow when the source lacks a clear gap, contribution, or supporting evidence. <br>


## Reference(s): <br>
- [PROCESS.md](artifact/PROCESS.md) <br>
- [TEMPLATE.md](artifact/TEMPLATE.md) <br>
- [sample-report.md](artifact/test-cases/sample-report.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/jack-long-2022/skills/paper-decompose) <br>
- [Publisher Profile](https://clawhub.ai/user/jack-long-2022) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown with structured sections and ASCII diagrams] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs include four required analysis layers and an optional investment-impact section for investment reports.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
