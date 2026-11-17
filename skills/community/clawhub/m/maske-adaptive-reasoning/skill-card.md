## Description:

自适应推理评估系统。自动评估任务复杂度并动态调整推理级别。在每次用户消息时触发，评估是否需要扩展思考（推理模式）来提高响应质量。用于复杂问题预处理。

This skill is ready for commercial/non-commercial use.

## Publisher:

[skillforge-jojo](https://clawhub.ai/user/skillforge-jojo)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to have an agent assess prompt complexity before each response and adjust response depth for complex tasks. It is intended for reasoning-heavy prompts such as planning, debugging, architecture review, mathematical reasoning, and high-stakes analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Always-on complexity assessment can change response depth for every prompt and may be distracting for users who prefer predictable, minimal responses.

Mitigation: Install only when adaptive response depth is desired, and disable or avoid the skill for workflows that require consistently brief output.

Risk: The skill may append reasoning-mode indicators to some responses.

Mitigation: Review generated responses before sharing them in contexts where visible indicators or style changes are undesirable.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/skillforge-jojo/skills/maske-adaptive-reasoning)
- [ClawHub publisher profile](https://clawhub.ai/user/skillforge-jojo)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown or plain text responses, optionally ending with reasoning-mode indicators for higher-complexity prompts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [No executable code, network access, credential access, file access, or persistence capability is present in the release evidence.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
