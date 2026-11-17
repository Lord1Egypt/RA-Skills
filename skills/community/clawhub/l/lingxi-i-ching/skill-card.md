## Description:

按中国传统六爻流程执行占卜：随机三钱起卦、排本卦变卦、计算日月建、给出用神与生克判断、生成通俗建议并保存历史。

This skill is ready for commercial/non-commercial use.

## Publisher:

[nycxk](https://clawhub.ai/user/nycxk)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents can use this skill to generate a structured Liu Yao reading, including hexagram casting, plate details, simplified date calculations, judgment, plain-language advice, and saved history for later review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Consultation questions and reading details are saved locally in plaintext history.

Mitigation: Avoid entering highly sensitive personal, medical, legal, financial, or relationship details unless the history file is managed, protected, or deleted.

Risk: The optional LLM mode can send the question and reading context to OpenAI.

Mitigation: Use --llm only when the user is willing to share that context with OpenAI; otherwise rely on the rule-based fallback.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/nycxk/skills/lingxi-i-ching)
- [Publisher profile](https://clawhub.ai/user/nycxk)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Console text with structured divination results, detailed line analysis, plain-language advice, and JSON Lines history entries.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Optional LLM-enhanced advice uses OPENAI_API_KEY and falls back to rule-based advice if the API call fails.]

## Skill Version(s):

1.0.0 (source: evidence.release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
