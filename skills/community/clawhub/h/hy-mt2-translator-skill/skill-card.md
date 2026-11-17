## Description:

This skill provides machine translation capabilities based on the Hy-MT2 model, supporting 38 languages and six translation modes for single text, multi-line files, and batch JSONL translation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tencent-adm](https://clawhub.ai/user/tencent-adm)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to translate text, structured content, files, and JSONL batches with terminology, style, delimiter-preservation, and context controls through Tencent Cloud or a user-hosted OpenAI-compatible backend.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores translation backend selection, model names, endpoint URLs, and API keys in agent memory.

Mitigation: Use a dedicated API key with limited scope, rotate it regularly, and delete remembered credentials and backend settings when the skill is no longer needed.

Risk: Source text, files, terminology, and contextual information can be sent to Tencent Cloud or a user-configured remote endpoint.

Mitigation: Avoid translating highly sensitive material unless the selected backend and data handling terms are acceptable for that content.

Risk: Users can override the Tencent endpoint URL or choose a private OpenAI-compatible backend.

Mitigation: Use only endpoints that the user or organization trusts, and prefer a private backend controlled by the deploying team for sensitive workloads.

## Reference(s):

- [Supported Languages](artifact/references/supported-languages.md)
- [Translation Modes Reference](artifact/references/translation-modes.md)
- [Tencent Cloud Hy-MT2 Model Detail](https://console.cloud.tencent.com/tokenhub/models/detail?modelId=hy-mt2-pro)
- [Tencent Hy-MT2 Hugging Face Collection](https://huggingface.co/collections/tencent/hy-mt2)
- [ClawHub Skill Page](https://clawhub.ai/tencent-adm/skills/hy-mt2-translator-skill)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Code, Configuration]

**Output Format:** [Markdown guidance with bash command blocks, translated text, and JSONL files for batch output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Single translations are returned as text; batch runs append translations to JSONL records and report success, failure counts, and output path.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
