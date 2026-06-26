## Description: <br>
Post to LinkedIn, comment, like, search organizations, and manage profiles via Pipedream OAuth integration. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[G9Pedro](https://clawhub.ai/user/G9Pedro) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to automate LinkedIn posting, comments, likes, organization search, profile lookup, and organization posting through Pipedream OAuth and pdauth. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can use local Pipedream credentials and hardcoded account details to post, comment, like, or delete public LinkedIn content. <br>
Mitigation: Use only LinkedIn, Pipedream, and organization accounts you control; replace hardcoded Telegram, auth provision, member, and organization IDs with verified values; require explicit confirmation before public content actions. <br>
Risk: Credential material from the pdauth configuration may be exposed if copied into scripts or committed with project files. <br>
Mitigation: Inspect ~/.config/pdauth/config.json before use, keep credentials local, and avoid committing copied credentials or account-specific identifiers. <br>


## Reference(s): <br>
- [Pipedream MCP](https://mcp.pipedream.com) <br>
- [LinkedIn API Docs](https://learn.microsoft.com/en-us/linkedin/marketing/) <br>
- [ClawHub Skill Page](https://clawhub.ai/G9Pedro/linkedin-pipedream) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Code, Configuration] <br>
**Output Format:** [Markdown instructions with bash and JavaScript snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses pdauth and Pipedream OAuth; organization posting includes a Node.js helper workaround.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
