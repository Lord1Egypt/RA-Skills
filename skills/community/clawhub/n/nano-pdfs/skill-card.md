## Description: <br>
Pub Nanopdf helps agents edit PDFs with natural-language instructions through the nano-pdf CLI and access SkillBoss models for generation, transcription, search, document parsing, email, and SMS. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[TobeyRebecca](https://clawhub.ai/user/TobeyRebecca) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and agents use this skill to call SkillBoss APIs for PDF/document workflows, multimodal model generation, chat, search, scraping, email, SMS, and related automation tasks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill is a broad external AI/API gateway presented under a PDF-focused name, so users may underestimate its scope. <br>
Mitigation: Install only when broad SkillBoss API access is intended, and review the available model, email, SMS, scraping, and paid-action capabilities before use. <br>
Risk: The skill can support email, SMS, batch messaging, scraping, and costly model actions. <br>
Mitigation: Require explicit user approval before any email, SMS, batch messaging, scraping, or paid model action, and use a limited or test API key where possible. <br>
Risk: Document parsing and model calls may send user content to external providers. <br>
Mitigation: Avoid sensitive documents unless approved, and confirm billing and provider data-handling expectations before processing user data. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/TobeyRebecca/nano-pdfs) <br>
- [SkillBoss Website](https://www.skillboss.co) <br>
- [SkillBoss API Base URL](https://api.heybossai.com/v1) <br>
- [Audio Models](audio-models.md) <br>
- [Chat Models](chat-models.md) <br>
- [Image Models](image-models.md) <br>
- [Search & Scraping Models](search-models.md) <br>
- [Tool Models](tools-models.md) <br>
- [Video Models](video-models.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and API request snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires SKILLBOSS_API_KEY and may return external API responses, generated media URLs, parsed document text, search results, email/SMS status, or model output.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
