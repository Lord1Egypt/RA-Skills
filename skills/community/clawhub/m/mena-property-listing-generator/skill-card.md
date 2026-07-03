## Description: <br>
Generates bilingual Arabic and English property listing copy and social-ready real estate content for MENA agents from basic property specs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jzargona](https://clawhub.ai/user/jzargona) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External real estate agents, agencies, property managers, and project sales teams use this skill to turn property specs into bilingual listing copy and channel-specific marketing or follow-up text for MENA markets. <br>

### Deployment Geography for Use: <br>
Middle East and North Africa (MENA) <br>

## Known Risks and Mitigations: <br>
Risk: Listing data, agent names, and phone numbers may be sent to an LLM when MINIMAX_API_KEY is set, and server security evidence says destination and credential behavior needs review. <br>
Mitigation: Review network and credential settings before installation; avoid private client or agent data until the publisher clearly declares allowed destinations and credential behavior. <br>
Risk: The skill stores listing records, agent profiles, and monthly counters under the user's local OpenClaw data directory. <br>
Mitigation: Treat local files as client and contact data; restrict filesystem access and remove saved records when they are no longer needed. <br>
Risk: Generated real estate copy may contain incorrect property facts, market claims, or platform-specific wording. <br>
Mitigation: Have a qualified agent review prices, details, compliance language, and platform requirements before publishing or sending generated content. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jzargona/skills/mena-property-listing-generator) <br>
- [MENA Property Listing Generator source skill](artifact/SKILL.md) <br>
- [Reference docs index](artifact/references/README.md) <br>
- [Marketing copy reference](artifact/references/marketing.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Configuration] <br>
**Output Format:** [Markdown and plain text listing content, with local JSON records for saved listings and agent profiles] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Bilingual Arabic and English real estate copy, social captions, short video scripts, WhatsApp follow-up text, and PDF-style listing descriptions.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
