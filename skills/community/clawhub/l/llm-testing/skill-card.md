## Description:

Provides curated prompts to test LLM security, bias, privacy, alignment, and robustness for authorized AI safety and red team assessments.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pandaai-1337](https://clawhub.ai/user/pandaai-1337)

### License/Terms of Use:

MIT-0

## Use Case:

Security researchers, AI safety engineers, red team operators, and developers use this skill to select prompt-based tests for LLM bias, privacy leakage, memory recall, alignment, and adversarial resistance. It is intended for authorized evaluations of models or systems the user owns or has permission to test.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The prompt corpus is designed for LLM red-team and safety testing and may elicit harmful, biased, privacy-invasive, or jailbreak-like responses when used against a target model.

Mitigation: Use only with explicit authorization, isolate the target model, and keep testing within a documented safety or security assessment scope.

Risk: Some prompts probe hidden instructions, filesystem listings, personal data, and memorized content, so raw model outputs may contain sensitive information.

Mitigation: Disable side-effecting tools where possible, set token and time limits, and avoid storing or sharing raw outputs that contain hidden prompts, directory listings, personal data, or harmful guidance.

Risk: Bias and demographic placeholders can produce offensive or discriminatory outputs if used carelessly or without review.

Mitigation: Replace placeholders deliberately, document the test methodology, review outputs in context, and handle findings through responsible disclosure or model-improvement workflows.

## Reference(s):

- [OWASP LLM Top 10](https://owasp.org/www-project-top-10-for-large-language-model-applications/)
- [AI Red Teaming Best Practices](https://www.anthropic.com/index/red-teaming-language-models)
- [Responsible AI Guidelines](https://www.partnershiponai.org/)
- [AI Safety Research](https://www.safe.ai/)
- [ClawHub skill page](https://clawhub.ai/pandaai-1337/skills/llm-testing)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Plain text and Markdown prompt lists with usage guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes placeholder-driven prompt sets for bias and memory testing; users replace placeholders before running tests.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
