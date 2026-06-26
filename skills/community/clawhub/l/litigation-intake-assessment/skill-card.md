## Description: <br>
Generates a China mainland litigation intake assessment report that structures case facts, evidence, claims, venue information, legal relationships, litigation risks, case-law research, and estimated win probability, timeline, and costs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[coolalam](https://clawhub.ai/user/coolalam) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Legal intake teams and dispute-resolution lawyers use this skill to prepare preliminary China mainland litigation assessments for case acceptance, evidence planning, risk review, and client expectation setting. <br>

### Deployment Geography for Use: <br>
China (Mainland) <br>

## Known Risks and Mitigations: <br>
Risk: The skill can send sensitive legal matter details and an API key to a third-party legal data service. <br>
Mitigation: Use redacted, non-confidential facts unless the user controls the API account and accepts the third-party data flow. <br>
Risk: The bundled search scripts disable normal HTTPS certificate verification. <br>
Mitigation: Fix TLS verification before using real credentials or client matter details. <br>
Risk: Generated litigation probabilities, timelines, costs, and intake recommendations may be incomplete when facts, evidence, or searches are limited. <br>
Mitigation: Treat outputs as preliminary and have a qualified reviewer verify assumptions, source materials, and current legal authorities before relying on them. <br>


## Reference(s): <br>
- [Assessment metrics](references/assessment-metrics.md) <br>
- [Prompt template](references/prompt-template.md) <br>
- [Search query patterns](references/search-query-patterns.md) <br>
- [Delilegal API key management](https://open.delilegal.com/personal/keys) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown report with optional shell command examples and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs are conditional legal-intake assessments and should preserve stated assumptions, evidence gaps, and search limitations.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
