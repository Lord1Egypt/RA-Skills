## Description: <br>
Provides curated prompts to test LLM security, bias, privacy, alignment, and robustness for authorized AI safety and red team assessments. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[PandaAI-1337](https://clawhub.ai/user/PandaAI-1337) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Security researchers, AI safety engineers, and red team operators use this skill to evaluate LLM behavior for bias, privacy leakage, alignment bypasses, and adversarial prompt resistance in authorized test environments. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill contains adversarial and sensitive LLM test prompts that could be misused outside authorized evaluation. <br>
Mitigation: Use only in authorized LLM safety or red-team assessments with written permission and responsible disclosure procedures. <br>
Risk: Submitting the prompts in an agent's own operating context could cause the agent to follow the tests rather than treat them as evaluation data. <br>
Mitigation: Run the prompts in a sandboxed test harness with sanitized context and a clearly separate target model. <br>
Risk: Privacy and data-leakage tests may elicit sensitive or personal-looking outputs from target systems. <br>
Mitigation: Avoid testing against sensitive local environments and do not share any personal data discovered during evaluation. <br>


## Reference(s): <br>
- [OWASP LLM Top 10](https://owasp.org/www-project-top-10-for-large-language-model-applications/) <br>
- [AI Red Teaming Best Practices](https://www.anthropic.com/index/red-teaming-language-models) <br>
- [Partnership on AI](https://www.partnershiponai.org/) <br>
- [Center for AI Safety](https://www.safe.ai/) <br>
- [ClawHub Skill Page](https://clawhub.ai/PandaAI-1337/llm-testing) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Markdown and plain-text prompt lists] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes placeholder-driven prompt sets for bias and memory recall testing.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
