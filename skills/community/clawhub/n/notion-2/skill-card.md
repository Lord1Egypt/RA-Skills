## Description: <br>
Integrates with Notion to search pages and databases, create, update, and archive pages, read and append block content, and query databases through the MorphixAI proxy. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[paul-leo](https://clawhub.ai/user/paul-leo) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to work with shared Notion workspaces: searching knowledge bases, reading page content, managing pages, and querying project databases. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can read and change Notion content that has been shared with the integration. <br>
Mitigation: Use a least-privilege Notion connection and share only the pages or databases needed for the task. <br>
Risk: A leaked MorphixAI API key could allow unauthorized use of the connected integration. <br>
Mitigation: Keep MORPHIXAI_API_KEY private and rotate it if exposure is suspected. <br>
Risk: Incorrect page, block, or database IDs could create, update, append, or archive the wrong Notion content. <br>
Mitigation: Verify target IDs and requested actions before mutating Notion pages or databases. <br>


## Reference(s): <br>
- [ClawHub Notion Skill](https://clawhub.ai/paul-leo/notion-2) <br>
- [MorphixAI API Keys](https://morphix.app/api-keys) <br>
- [MorphixAI Connections](https://morphix.app/connections) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown with YAML-like tool call examples and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires MORPHIXAI_API_KEY, a linked MorphixAI connection, and Notion pages or databases shared with the integration.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
