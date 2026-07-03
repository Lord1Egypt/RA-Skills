## Description: <br>
Integrates NLP models, benchmarks, and large language datasets for model lookup, evaluation, question answering, translation, and corpus extraction through API-oriented workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ai-gaoqian](https://clawhub.ai/user/ai-gaoqian) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and NLP practitioners use this skill to route requests across HuggingFace model metadata, GLUE and MMLU evaluation, SQuAD question answering, FLORES translation, and corpus extraction from FineWeb, C4, and The Pile. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill describes access to third-party models and large language datasets that may carry separate licensing, copyright, or content restrictions. <br>
Mitigation: Confirm the applicable model and dataset terms before use, and apply content review or filtering appropriate to the deployment. <br>
Risk: HuggingFace model access may require an HF_TOKEN credential. <br>
Mitigation: Use a scoped token, store it outside shared prompts or logs, and rotate it if exposure is suspected. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ai-gaoqian/skills/nlp-api-hub) <br>
- [Publisher profile](https://clawhub.ai/user/ai-gaoqian) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, Guidance, Text] <br>
**Output Format:** [Markdown with API endpoint descriptions and request parameter guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May require an HF_TOKEN for HuggingFace model access; users remain responsible for dataset licensing, copyright, and content compliance.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
