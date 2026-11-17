## Description:

Translate content across multiple platforms and languages with context-aware localization.

This skill is ready for commercial/non-commercial use.

## Publisher:

[paudyyin](https://clawhub.ai/user/paudyyin)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to translate Chinese and English content, select a translation engine, and apply localization guidance for terminology, tone, and review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill documentation says text stays local, but the security evidence states that text is sent to external translation and chat services.

Mitigation: Do not use the skill for passwords, API keys, personal data, confidential business text, legal documents, or regulated material unless the user accepts transmission to the selected provider.

Risk: Fallback behavior can send content to a different provider than the user originally selected.

Mitigation: Require explicit confirmation before using fallback providers and disclose which provider will receive the text.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/paudyyin/skills/multi-platform-translator)
- [Publisher profile](https://clawhub.ai/user/paudyyin)
- [iFlytek translation](https://fanyi.xfyun.cn/console/trans/text)
- [DeepL translator](https://www.deepl.com/zh/translator)
- [iCIBA](https://www.iciba.com/)
- [Doubao chat](https://www.doubao.com/chat)
- [Tencent Yuanbao chat](https://yuanbao.tencent.com/chat/naQivTmsDa)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Plain text or Markdown translation responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Single-stream response with optional translation brief, draft, review notes, and terminology guidance.]

## Skill Version(s):

1.2.0 (source: server release evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
