## Description:

将正常中文文本转换为火星文（2005-2010年代非主流网络文体），使用611个汉字映射生成可辨认的非主流风格文本。

This skill is ready for commercial/non-commercial use.

## Publisher:

[cantoneyes](https://clawhub.ai/user/cantoneyes)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to convert normal Chinese text into nostalgic 2005-2010-era 火星文 for novelty, social, or stylistic text generation. Developers can run the bundled CLI to create seeded examples, adjust conversion probability, or inspect character mappings.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The documented --json flag currently appears broken because the script uses json.dumps without importing json.

Mitigation: Use plain text output for current releases, or add and verify the missing json import before relying on JSON output.

Risk: The documentation and CLI messages are in Chinese, which can limit operator review for non-Chinese readers.

Mitigation: Have a Chinese-reading reviewer validate prompts, CLI output, and generated text before deployment in multilingual workflows.

Risk: Random replacement can make outputs vary between runs.

Mitigation: Use --seed for reproducible examples and --prob to control how much of the source text is transformed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cantoneyes/skills/mars-text-translator)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Guidance]

**Output Format:** [Plain text conversion output with Markdown usage guidance and bash command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Random replacement is controllable with --prob and reproducible with --seed; the documented --json flag may fail until the missing json import is added.]

## Skill Version(s):

2.1.0 (source: server release evidence and README version history)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
