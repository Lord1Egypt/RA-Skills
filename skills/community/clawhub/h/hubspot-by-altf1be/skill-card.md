## Description: <br>
Full HubSpot platform CLI for CRM contacts, companies, deals, tickets, CMS blog posts and pages, marketing emails, forms, lists, conversations, and automation workflows using Private App token or OAuth 2.0 authentication. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Abdelkrim](https://clawhub.ai/user/Abdelkrim) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and business automation teams use this skill to let an agent inspect and manage HubSpot CRM, CMS, marketing, conversations, and workflow resources through a Node.js command-line interface. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can read and modify HubSpot CRM, CMS, marketing, conversations, and workflow data when granted broad app scopes. <br>
Mitigation: Use a dedicated HubSpot Private App or OAuth app with the least scopes needed for the intended workflow. <br>
Risk: Write and delete commands can change or remove business records. <br>
Mitigation: Review agent-proposed write and delete commands before execution; delete commands require an explicit --confirm flag. <br>
Risk: HubSpot credentials in environment files or OAuth token cache files can expose account access. <br>
Mitigation: Protect .env files, avoid sharing logs or workspaces containing secrets, and secure or remove ~/.cache/openclaw/hubspot-token.json when OAuth mode is used. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Abdelkrim/hubspot-by-altf1be) <br>
- [HubSpot Developers](https://developers.hubspot.com/) <br>
- [Command reference](SKILL.md) <br>
- [HubSpot API coverage and limitations](docs/API-COVERAGE.md) <br>
- [README](README.md) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Text, JSON, Guidance] <br>
**Output Format:** [CLI text and JSON responses with Markdown command examples in the skill documentation] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js >= 18 and HubSpot credentials; command result sizes can be limited with HUBSPOT_MAX_RESULTS.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
