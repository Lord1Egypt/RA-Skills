## Description: <br>
Tencent Hy-MT2-Translator provides Hy-MT2-based machine translation across 38 supported languages with basic, terminology-constrained, style-controlled, delimiter-preserving, structured-data, context-aware, file, and batch JSONL workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tencent-adm](https://clawhub.ai/user/tencent-adm) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and localization teams use this skill to translate text, documents, structured content, and batch JSONL files through Tencent Cloud Hy-MT2 or a user-hosted OpenAI-compatible translation backend. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Stored API keys, backend URLs, model names, and active backend choices can be reused across sessions. <br>
Mitigation: Use limited-scope API keys, clear stored credentials when changing backends, and rotate keys when access is no longer needed. <br>
Risk: Sensitive text may be sent to the previously selected backend without a fresh confirmation. <br>
Mitigation: Confirm the active backend and data approval status before translating confidential or regulated content. <br>
Risk: Custom private-model endpoints can send translation data to untrusted infrastructure. <br>
Mitigation: Use only trusted, approved OpenAI-compatible endpoints and avoid unverified backend URLs. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/tencent-adm/hy-mt2-translator-skill) <br>
- [Tencent Cloud Hy-MT2 model detail](https://console.cloud.tencent.com/tokenhub/models/detail?modelId=hy-mt2-pro) <br>
- [Tencent Hy-MT2 Hugging Face collection](https://huggingface.co/collections/tencent/hy-mt2) <br>
- [Supported Languages](references/supported-languages.md) <br>
- [Translation Modes Reference](references/translation-modes.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Plain translated text for single requests; JSONL files with added translation fields for batch jobs; Markdown guidance and shell commands for setup and execution.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May call Tencent Cloud or a user-hosted OpenAI-compatible backend. Batch mode supports resumable JSONL output.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
