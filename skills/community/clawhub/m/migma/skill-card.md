## Description: <br>
Generate, send, validate, and export AI-powered emails from the terminal; manage contacts, segments, tags, domains, and webhooks with Migma CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[AdamSEY](https://clawhub.ai/user/AdamSEY) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Marketing operators, founders, and developers use this skill through an agent to create branded email campaigns, validate deliverability, send test or production messages, export to email platforms, and manage audience data with the Migma CLI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can send real email, including to segments or tags. <br>
Mitigation: Require the agent to show the subject, sender, audience or segment, and a test or preview result before any real or bulk send. <br>
Risk: Contact import and list management can upload or change contact data. <br>
Mitigation: Review contact CSVs and confirm target contacts, segments, or tags before import, removal, or campaign actions. <br>
Risk: MIGMA_API_KEY enables account actions through the Migma CLI. <br>
Mitigation: Protect the API key and install only if you trust Migma and the @migma/cli package. <br>


## Reference(s): <br>
- [Migma homepage](https://migma.ai) <br>
- [Example Conversations](references/workflows.md) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance, JSON, Files] <br>
**Output Format:** [Markdown with inline bash and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses --json for structured CLI responses; may save generated email HTML, PDF, or MJML files when requested.] <br>

## Skill Version(s): <br>
1.3.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
