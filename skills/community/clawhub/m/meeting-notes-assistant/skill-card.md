## Description: <br>
Meeting Notes Assistant transcribes meeting audio with local Whisper, generates structured notes and action items, and exports Word, PDF, email, and Feishu-ready outputs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[liugouxiong](https://clawhub.ai/user/liugouxiong) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees and teams use this skill to convert authorized meeting recordings or transcripts into structured notes, action items, searchable local records, and shareable documents. It is most relevant when local transcription is preferred, with optional LLM or cloud ASR settings available for richer analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Sensitive meeting audio or transcripts may be sent to external AI or cloud ASR services when optional LLM or cloud features are configured. <br>
Mitigation: For confidential meetings, run local transcription, use --no-llm, avoid setting OPENAI_API_KEY or OPENAI_API_BASE, and keep outputs in a secure local folder. <br>
Risk: Transcription or summarization errors can misstate decisions, names, dates, numbers, or action items. <br>
Mitigation: Review generated transcripts and notes before distributing them or relying on them for business decisions. <br>
Risk: Recording or processing meetings without permission can create privacy or legal issues. <br>
Mitigation: Use the skill only for authorized recordings and follow applicable consent, retention, and workplace policies. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/liugouxiong/meeting-notes-assistant) <br>
- [User Guide](USER_GUIDE.md) <br>
- [Privacy Statement](PRIVACY.md) <br>
- [Domain Adaptive Architecture](docs/domain-adaptive-architecture.md) <br>
- [Universal Domain Recognition Plan](docs/universal-domain-recognition-plan.md) <br>
- [Word Template Guide](references/template_guide.md) <br>
- [Whisper large-v3 model download](https://openaipublic.azureedge.net/main/whisper/large-v3.pt) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, configuration, files] <br>
**Output Format:** [Markdown guidance with shell commands, plus generated transcript text, structured notes JSON, DOCX/PDF files, and email or Feishu payloads.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May store meeting data under ~/.workbuddy and may call configured OpenAI-compatible LLM or cloud ASR providers unless offline or no-LLM operation is selected.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter, release metadata, changelog released 2026-04-08) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
