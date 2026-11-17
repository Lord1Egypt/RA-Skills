## Description:

Meeting Notes Assistant transcribes meeting audio with local Whisper, generates structured meeting notes with topics, decisions, action items, and keywords, and exports results to Word, PDF, Feishu-ready payloads, or email-ready files.

This skill is ready for commercial/non-commercial use.

## Publisher:

[liugouxiong](https://clawhub.ai/user/liugouxiong)

### License/Terms of Use:

MIT

## Use Case:

Employees, external users, and teams use this skill to turn meeting recordings, transcripts, documents, or links into structured notes for archiving, review, and follow-up task distribution. It is especially suited for business meetings where local transcription, searchable history, and document export are useful.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill presents local/private transcription, but notes generation can send sensitive transcripts to an external OpenAI-compatible LLM API when configured.

Mitigation: For confidential meetings, use local transcription with the rule-based fallback, run with --no-llm, and avoid setting OPENAI_API_KEY or llm_api_key unless external processing is approved.

Risk: Meeting transcripts and summaries may contain private or regulated information.

Mitigation: Use the skill only for recordings where participants have given appropriate consent, keep generated files in controlled local storage, and review third-party provider privacy terms before enabling cloud services.

Risk: Transcription and summarization may misrecognize names, numbers, dates, or domain-specific terminology.

Mitigation: Review important notes manually before distribution, prefer higher-accuracy models for formal records, and maintain domain dictionaries for specialized terms.

Risk: PDF export from untrusted notes may be unsafe until HTML escaping and resource blocking are fixed.

Mitigation: Be cautious when exporting PDF from untrusted note content and review or sanitize note inputs before conversion.

## Reference(s):

- [Template Guide](artifact/references/template_guide.md)
- [Domain-Adaptive Architecture](artifact/docs/domain-adaptive-architecture.md)
- [Universal Domain Recognition Plan](artifact/docs/universal-domain-recognition-plan.md)
- [Whisper large-v3 model download](https://openaipublic.azureedge.net/main/whisper/large-v3.pt)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance, shell commands, JSON meeting notes, transcript text, Word/PDF document files, and Feishu/email-ready export payloads]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May store local transcripts, notes, templates, and meeting history under the user's WorkBuddy configuration directories.]

## Skill Version(s):

1.0.0 (source: frontmatter, changelog, release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
