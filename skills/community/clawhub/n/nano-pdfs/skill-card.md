## Description:

Pub Nanopdf helps agents edit PDFs with natural-language instructions through the nano-pdf CLI and access SkillBoss API models for media generation, chat, search, document parsing, email, and SMS.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tobeyrebecca](https://clawhub.ai/user/tobeyrebecca)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users can use this skill to have an agent draft shell commands and API requests for PDF/document processing and broader SkillBoss model calls, including chat, media generation, search, email, and SMS.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts, documents, media, URLs, phone numbers, and message contents can be sent to an external service and downstream providers.

Mitigation: Use a restricted API key and avoid sensitive or regulated data unless those services are approved for that data.

Risk: The skill supports email, SMS, scraping, and file-writing workflows.

Mitigation: Require manual confirmation before outbound messages, scraping, downloads, or local file writes.

Risk: The release is broader than PDF editing and functions as a general SkillBoss API gateway.

Mitigation: Install it only when the broader gateway behavior is intended and limit use to expected model categories.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tobeyrebecca/skills/nano-pdfs)
- [SkillBoss](https://www.skillboss.co)
- [SkillBoss API base URL](https://api.heybossai.com/v1)
- [Audio Models](audio-models.md)
- [Chat Models](chat-models.md)
- [Image Models](image-models.md)
- [Search & Scraping Models](search-models.md)
- [Tool Models](tools-models.md)
- [Video Models](video-models.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with bash and curl examples, API request bodies, and model identifiers.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires SKILLBOSS_API_KEY; outputs may trigger external API calls and downstream provider processing.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
