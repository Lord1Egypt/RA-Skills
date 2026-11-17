## Description:

Guides Chinese-speaking users through Role-Task-Format-CoT prompt design, prompt diagnosis, model adaptation, and structured output control for GPT, Claude, Gemini, and Chinese large language models.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qqyougitcom](https://clawhub.ai/user/qqyougitcom)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to diagnose weak prompts and produce Chinese-language prompt templates, examples, constraints, and model-specific tuning guidance for common AI workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad prompt-related trigger language may route more requests to this skill than intended.

Mitigation: Review and narrow activation terms before deployment when routing precision is important.

Risk: The skill is designed to answer in Chinese, which may not match every user's language preference.

Mitigation: Set explicit language preferences or adapt the output-language instruction for multilingual deployments.

Risk: Prompt recommendations can still produce weak or misleading downstream model behavior if adopted without testing.

Mitigation: Validate generated prompts with representative, boundary, and repeatability test cases before relying on them.

## Reference(s):

- [Detailed Prompt Engineering Reference](artifact/references/details.md)
- [ClawHub skill page](https://clawhub.ai/qqyougitcom/skills/mimo-prompt-engineering-expert)

## Skill Output:

**Output Type(s):** [text, markdown, guidance, configuration]

**Output Format:** [Chinese-language Markdown with prompt templates, diagnostic tables, examples, and model settings]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include JSON, Markdown table, XML, and structured prompt examples when useful.]

## Skill Version(s):

1.4.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
