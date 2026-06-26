## Description: <br>
Generates I Ching divination readings from natural-language questions by running a local hexagram script, consulting built-in Zhouyi references, and using web research to produce a structured interpretation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[crystalchen1017](https://clawhub.ai/user/crystalchen1017) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to cast and interpret I Ching hexagrams from natural-language questions, including Chinese-language readings that combine local reference material with online source checking. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Divination questions or web searches may expose sensitive personal details. <br>
Mitigation: Avoid including sensitive personal information in questions and keep prompts focused on the decision context. <br>
Risk: I Ching readings can be mistaken for factual, medical, legal, financial, or other professional advice. <br>
Mitigation: Treat outputs as interpretive reference and use qualified professional guidance for consequential decisions. <br>
Risk: The skill runs a local Python script and may perform web searches using the question or hexagram terms. <br>
Mitigation: Review the script and generated search terms before use in restricted environments. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/crystalchen1017/gua) <br>
- [Output format](references/output-format.md) <br>
- [Pre-divination guidance](references/pre-divination-guidance.md) <br>
- [Zhouyi 64-hexagram local reference](references/zhouyi-64-gua.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown with command output, hexagram text diagrams, citations, and structured interpretation sections] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The reading includes the original question, primary and changed hexagrams, moving-line basis, targeted interpretation, and reference links.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
