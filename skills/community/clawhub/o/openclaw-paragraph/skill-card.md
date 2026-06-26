## Description: <br>
OpenClaw skill for Paragraph.com, enabling agents to create, retrieve, and list Web3-native blog posts, manage subscribers, and inspect tokenized post data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ClaireAICodes](https://clawhub.ai/user/ClaireAICodes) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External creators, DAOs, Web3 projects, and developers use this skill to automate Paragraph publishing workflows, manage publication subscribers, and retrieve post, feed, user, and token data through an OpenClaw agent. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can publish public or onchain Paragraph posts and optionally send newsletters. <br>
Mitigation: Install only for publications you control and require human approval before publishing or sending newsletters. <br>
Risk: The skill can add, list, and import subscribers, including emails and wallet addresses. <br>
Mitigation: Use a dedicated API key where possible, handle subscriber data as personal data, and import only vetted subscriber lists. <br>
Risk: The subscriber import flow accepts a caller-chosen local CSV file path. <br>
Mitigation: Allow imports only from trusted local paths and review the CSV contents before execution. <br>
Risk: Welcome emails may be sent during subscriber operations. <br>
Mitigation: Set sendWelcomeEmail deliberately for each workflow and require review before bulk subscriber imports. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/ClaireAICodes/openclaw-paragraph) <br>
- [Publisher profile](https://clawhub.ai/user/ClaireAICodes) <br>
- [Paragraph API documentation](https://paragraph.com/docs/api-reference) <br>
- [Paragraph](https://paragraph.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance] <br>
**Output Format:** [JSON tool responses and Markdown content sent to Paragraph APIs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create public or onchain Paragraph posts, send newsletters, import subscriber CSV files, and return publication, subscriber, feed, user, and coin data.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release metadata, SKILL.md frontmatter, package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
