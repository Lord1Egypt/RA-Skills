## Description:

Pub Pdf helps agents use a SkillBoss API key to call remote PDF/document processing, chat, media generation, search, email, SMS, and related model workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[alvisdunlop](https://clawhub.ai/user/alvisdunlop)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to discover and call SkillBoss-hosted model and tool endpoints for PDFs, document parsing, generation, search, communication, and media workflows. It is suited to workflows that intentionally allow remote processing with a SkillBoss API key.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill exposes broader remote API capabilities than the PDF-oriented name suggests, including email, SMS, media generation, search, and document upload.

Mitigation: Install it only for workflows that explicitly require broad SkillBoss API access, and review requested actions before allowing communication, upload, or web/search operations.

Risk: Inputs may be sent to remote services through SkillBoss endpoints.

Mitigation: Avoid confidential documents, recordings, contact lists, email/SMS workflows, and OTP flows unless separate approval and data-handling controls are in place.

Risk: The skill requires SKILLBOSS_API_KEY, which can authorize remote model and tool calls.

Mitigation: Scope, store, and rotate the API key according to local credential policy, and provide it only in environments intended for SkillBoss use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/alvisdunlop/skills/pdfs)
- [Publisher profile](https://clawhub.ai/user/alvisdunlop)
- [SkillBoss website](https://www.skillboss.co)
- [SkillBoss API base URL](https://api.heybossai.com/v1)
- [Chat model reference](artifact/chat-models.md)
- [Image model reference](artifact/image-models.md)
- [Audio model reference](artifact/audio-models.md)
- [Search and scraping model reference](artifact/search-models.md)
- [Tool model reference](artifact/tools-models.md)
- [Video model reference](artifact/video-models.md)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, code, text, markdown]

**Output Format:** [Markdown guidance with API examples and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires SKILLBOSS_API_KEY and sends selected inputs to remote SkillBoss endpoints.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
