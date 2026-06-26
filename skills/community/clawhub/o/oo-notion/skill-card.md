## Description: <br>
This skill lets agents read, create, update, move, archive, and delete Notion workspace content through the OOMOL-connected Notion connector. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to operate Notion from an agent after connecting a Notion account through OOMOL. It supports schema-first read workflows and confirmed write or destructive changes to pages, blocks, databases, data sources, users, and Markdown content. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can use a connected Notion account for broad read and write operations. <br>
Mitigation: Install only when agent access to that Notion account is intended, and give explicit instructions for create or update tasks. <br>
Risk: Write and destructive actions can change, archive, trash, or delete Notion content. <br>
Mitigation: Review the proposed target, payload, and expected effect before allowing write or destructive actions to run. <br>
Risk: The skill requires OAuth or other sensitive connected-account credentials through OOMOL. <br>
Mitigation: Keep credentials managed through the OOMOL connection flow and avoid exposing raw tokens in prompts, files, or shell output. <br>


## Reference(s): <br>
- [ClawHub Notion skill page](https://clawhub.ai/oomol/oo-notion) <br>
- [OOMOL publisher profile](https://clawhub.ai/user/oomol) <br>
- [oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [Notion homepage](https://www.notion.so) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration instructions, API Calls, JSON, Markdown, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON connector payloads or responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Connector responses include data and execution metadata when actions run successfully.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
