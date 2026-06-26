## Description: <br>
Official skill for how to use karakeep (the bookmark manager) and interact with it programmatically. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[karakeep](https://clawhub.ai/user/karakeep) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to operate a Karakeep instance through the CLI, including adding, searching, organizing, updating, and deleting bookmarks, lists, and tags. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a Karakeep API key, which could expose account access if mishandled. <br>
Mitigation: Use a revocable API key, provide it through environment variables, and avoid passing secrets on the command line. <br>
Risk: The skill includes commands that can delete bookmarks or lists. <br>
Mitigation: Require explicit user confirmation before running delete commands or other destructive account changes. <br>
Risk: The security review notes that the example cloud server address may not match current official Karakeep documentation. <br>
Mitigation: Set the server address from the user's own instance or current official Karakeep documentation before use. <br>


## Reference(s): <br>
- [Karakeep homepage](https://karakeep.app) <br>
- [Karakeep documentation](https://docs.karakeep.app) <br>
- [Karakeep repository](https://github.com/karakeep-app/karakeep) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline bash code blocks and CLI examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes CLI usage patterns for Karakeep and may reference JSON output from the CLI.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
