## Description: <br>
Access Paragraph.com Web3-native blogging to create, fetch, and manage onchain posts, publications, subscribers, and tokenized content via API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ClaireAICodes](https://clawhub.ai/user/ClaireAICodes) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Creators, developers, DAOs, and Web3 teams use this skill to automate Paragraph publishing workflows, manage subscribers, inspect publications, and retrieve tokenized post or feed data through an agent. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can publish posts, send newsletter or welcome emails, and manage subscribers through a live Paragraph account. <br>
Mitigation: Require human review before publishing posts, importing subscriber CSVs, or sending emails. <br>
Risk: Subscriber imports can expose or upload email and wallet data that the user may not be authorized to process. <br>
Mitigation: Use only subscriber data the operator is authorized to upload and contact, and keep API keys least-privilege and revocable. <br>
Risk: CSV import behavior depends on agent filesystem access and selected file paths. <br>
Mitigation: Install only where the agent has limited filesystem access and review import paths and CSV contents before execution. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/ClaireAICodes/paragraph-skill) <br>
- [Paragraph API Reference](https://paragraph.com/docs/api-reference) <br>
- [Paragraph](https://paragraph.com) <br>
- [Node.js](https://nodejs.org) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, API calls, configuration, guidance] <br>
**Output Format:** [JSON tool responses with success, data, and error fields; published post content is supplied as Markdown.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Paragraph API credentials and can create external publishing, email, and subscriber-management side effects.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release evidence, SKILL.md frontmatter, package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
