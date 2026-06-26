## Description: <br>
Access and manage Web3-native blogging on Paragraph.com with onchain posts, tokenized content, subscriber management, and automated publishing via API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ClaireAICodes](https://clawhub.ai/user/ClaireAICodes) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External creators, DAOs, Web3 projects, and developers use this tool to let agents publish Markdown posts, manage subscribers, and inspect Paragraph publications, posts, users, feeds, and tokenized post data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Agents can create public posts, trigger newsletter sends, and manage subscriber relationships through the Paragraph API. <br>
Mitigation: Require explicit human approval before creating posts, sending newsletters, adding subscribers, or importing subscriber lists. <br>
Risk: Subscriber import can process local CSV files containing personal data or contact information. <br>
Mitigation: Only import CSV files that have been verified, are authorized for processing, and match the expected subscriber format. <br>
Risk: A custom PARAGRAPH_API_BASE_URL can send credentials or content to an untrusted endpoint. <br>
Mitigation: Keep PARAGRAPH_API_BASE_URL pointed at Paragraph or a trusted test endpoint. <br>
Risk: Broad Paragraph API credentials can give an agent powerful publishing and subscriber-management access. <br>
Mitigation: Use a dedicated or least-privileged API key where available and store it outside prompts or generated content. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ClaireAICodes/paragraph-test) <br>
- [Paragraph API reference](https://paragraph.com/docs/api-reference) <br>
- [Paragraph](https://paragraph.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, API responses] <br>
**Output Format:** [Structured tool results with success, data, and error fields; Markdown content may be sent to Paragraph when creating posts.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires PARAGRAPH_API_KEY and PARAGRAPH_PUBLICATION_SLUG; can read local CSV files for subscriber import and can use a configurable Paragraph API base URL.] <br>

## Skill Version(s): <br>
1.2.0 (source: ClawHub release metadata, SKILL.md frontmatter, package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
