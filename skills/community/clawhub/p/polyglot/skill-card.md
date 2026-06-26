## Description: <br>
Translate text to any language with formality control and cultural notes. Target language defaults to English. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[unixlamadev-spec](https://clawhub.ai/user/unixlamadev-spec) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use Polyglot to translate messages, documents, and other text while controlling formality and receiving cultural or idiomatic notes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Input text is sent to AIProx and downstream model providers for translation. <br>
Mitigation: Use the skill only for text approved for external processing. <br>
Risk: The skill requires an AIProx spend token for paid API access. <br>
Mitigation: Keep the spend token secret, prefer scoped or revocable tokens, and monitor usage or billing. <br>


## Reference(s): <br>
- [AIProx homepage](https://aiprox.dev) <br>


## Skill Output: <br>
**Output Type(s):** [text, guidance] <br>
**Output Format:** [Structured text or JSON-style translation response] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include translated text, detected source language, target language, formality level, and cultural notes.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
