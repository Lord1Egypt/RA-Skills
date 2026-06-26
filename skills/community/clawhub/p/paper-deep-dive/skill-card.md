## Description: <br>
Paper Deep Dive helps an agent produce structured, evidence-driven analyses of a single academic paper, including research context, method walkthroughs, claim-to-evidence mapping, and limitations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tom-zju](https://clawhub.ai/user/tom-zju) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Researchers, students, engineers, and technical readers use this skill to turn a focal paper, PDF, arXiv page, appendix, project page, or title-and-abstract input into a rigorous deep dive. It is intended for blog-quality explainers, group discussion preparation, research-context mapping, method analysis, and checking whether experiments support the paper's claims. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can produce incorrect, incomplete, or overconfident analysis of a paper's claims, methods, or experiments. <br>
Mitigation: Treat outputs as analysis aids, verify important claims against the original paper, and preserve explicit evidence labels and uncertainty markers. <br>
Risk: Inputs may include private drafts, confidential research, or unreleased code. <br>
Mitigation: Provide sensitive materials only to an agent/runtime approved to process them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/tom-zju/paper-deep-dive) <br>
- [Evidence rules](references/evidence-rules.md) <br>
- [Output template](references/output-template.md) <br>
- [Paper types](references/paper-types.md) <br>
- [Quick reference](references/quickref.md) <br>
- [Visualization guide](references/visualization.md) <br>
- [Attention paper example](references/example-attention.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Structured Markdown with tables and optional Mermaid diagrams] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include evidence labels, claim-to-evidence tables, formulas, and Mermaid diagrams; output depth depends on the quality and completeness of the paper sources provided.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
