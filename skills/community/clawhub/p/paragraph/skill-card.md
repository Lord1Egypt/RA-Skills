## Description: <br>
OpenClaw skill for Paragraph.com - Web3-native blogging with tokenization, onchain storage, and community features. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ClaireAICodes](https://clawhub.ai/user/ClaireAICodes) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External creators, DAOs, Web3 teams, and developers use this skill to let an agent create Paragraph posts, inspect publications and feeds, manage subscribers, and query token or coin data through Paragraph's API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can let an agent publish Paragraph content that may become public, emailed, or onchain and difficult to fully undo. <br>
Mitigation: Review every post before publishing, leave newsletter sending disabled unless intentional, and treat published/onchain content as persistent. <br>
Risk: Subscriber import and email-related actions can affect real contacts and may involve consent-sensitive data. <br>
Mitigation: Import only authorized and consented subscriber data, validate CSV contents before use, and disable welcome emails unless messages are intended. <br>
Risk: The Paragraph API key gives the agent operational authority over the connected Paragraph account. <br>
Mitigation: Use a scoped and revocable API key, store it only in the agent environment, rotate it when needed, and remove access when automation is no longer required. <br>


## Reference(s): <br>
- [ClawHub Paragraph Skill Page](https://clawhub.ai/ClaireAICodes/paragraph) <br>
- [Paragraph API Reference](https://paragraph.com/docs/api-reference) <br>
- [Paragraph](https://paragraph.com) <br>
- [Node.js](https://nodejs.org) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance] <br>
**Output Format:** [JSON tool results and Markdown content submitted to Paragraph] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires PARAGRAPH_API_KEY and PARAGRAPH_PUBLICATION_SLUG; tools return standardized success, data, and error fields.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release metadata, SKILL.md frontmatter, and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
