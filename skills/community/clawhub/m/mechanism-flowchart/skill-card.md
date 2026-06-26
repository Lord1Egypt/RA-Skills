## Description: <br>
Generates Mermaid flowchart code and visual representations of medical mechanisms, pathophysiology, and drug action pathways. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aipoch-ai](https://clawhub.ai/user/aipoch-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, educators, and medical-content authors use this skill to turn supplied mechanism or pathway text into Mermaid flowchart code and diagram metadata for educational diagrams, presentation figures, and pathway visualization. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated mechanism diagrams may be mistaken for medical advice or clinical decision support. <br>
Mitigation: Use the skill only for non-sensitive educational or publication diagram drafting, and review outputs with qualified domain judgment before use. <br>
Risk: The local Python script and unpinned dependencies create dependency hygiene and execution-review needs. <br>
Mitigation: Review the script before running it, execute it in a controlled workspace, and avoid installing unnecessary unpinned dependencies. <br>
Risk: Complex or stress-case pathway inputs can produce weaker boundary handling or diagrams that need refinement. <br>
Mitigation: Keep prompts scoped to supplied mechanism or pathway text, validate assumptions explicitly, and manually refine complex mechanisms. <br>


## Reference(s): <br>
- [Mechanism Flowchart Skill Page](https://clawhub.ai/aipoch-ai/mechanism-flowchart) <br>
- [Mechanism Flowchart Guidelines](references/guidelines.md) <br>
- [Mermaid Documentation](https://mermaid.js.org/intro/) <br>
- [Mermaid Flowchart Syntax](https://mermaid.js.org/syntax/flowchart.html) <br>
- [Mermaid Live Editor](https://mermaid.live/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, JSON, Shell commands, Guidance] <br>
**Output Format:** [Markdown with Mermaid code blocks and JSON metadata] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Mermaid visualization requires a Mermaid renderer, and generated medical pathway diagrams should be manually reviewed for accuracy.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
