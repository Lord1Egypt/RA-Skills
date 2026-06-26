## Description: <br>
Generates high-confidence, source-traceable, structured industry definition reports for a user-provided industry or product term. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[youhaokun0514-sys](https://clawhub.ai/user/youhaokun0514-sys) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and research teams use this skill to normalize industry or product names, classify them with an L1-L5 scheme, route retrieval, clean source material, and produce a structured definition report with source citations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The bundled search path can produce simulated retrieval results, which may look like source-backed research without actually verifying external evidence. <br>
Mitigation: Use real retrieval in place of the mock search path and manually verify every cited source before relying on reports for business, regulatory, investment, or other consequential decisions. <br>


## Reference(s): <br>
- [L1-L5 Classification](references/l1-l5-classification.md) <br>
- [Four-Structure Template](references/four-structure-template.md) <br>
- [Source Tracing](references/source-tracing.md) <br>
- [LLM-as-a-Judge Quality Assessment](references/LLM-as-a-Judge.md) <br>
- [Skill Page](https://clawhub.ai/youhaokun0514-sys/industry-intro) <br>
- [China National Standards Public Service Platform](https://openstd.samr.gov.cn/) <br>
- [China Association of Automobile Manufacturers](https://www.caam.org.cn/) <br>
- [Pharmacopoeia of the People's Republic of China](https://www.chp.org.cn/) <br>
- [China Pharmaceutical Industry Association](https://www.pharmtec.org.cn/) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Analysis, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown report with classification, definition content, numbered source citations, and source list] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs should preserve key numeric values, avoid vague or promotional phrasing, and include source markers for key claims.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
