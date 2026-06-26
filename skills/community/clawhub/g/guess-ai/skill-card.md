## Description: <br>
OceanBus-powered social deduction game for hosting or joining a multiplayer Who's the AI? party over OceanBus P2P messaging. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ryanbihai](https://clawhub.ai/user/ryanbihai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to host or join a command-line multiplayer social deduction game where players communicate through OceanBus P2P messaging, assign roles, speak in rounds, vote, and optionally use LLM-powered AI host or player modes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The package includes an unrelated service-registration script and was assessed as suspicious by the security evidence. <br>
Mitigation: Review before installing or running, and do not run register-lobster.js unless you intentionally want to publish a Captain Lobster Yellow Pages entry. <br>
Risk: AI modes may send gameplay content to Anthropic when ANTHROPIC_API_KEY is configured. <br>
Mitigation: Use AI host and AI player modes only with player consent, and avoid sharing sensitive gameplay content. <br>
Risk: OceanBus credentials and identity data are stored under ~/.oceanbus. <br>
Mitigation: Treat files under ~/.oceanbus as sensitive credentials and avoid sharing or committing them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ryanbihai/guess-ai) <br>
- [Configured homepage](https://github.com/ryanbihai/guess-ai) <br>
- [OceanBus package](https://www.npmjs.com/package/oceanbus) <br>
- [README](artifact/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and game messages] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [AI host and AI player modes require an LLM API key; OceanBus identity and roster data are stored under ~/.oceanbus.] <br>

## Skill Version(s): <br>
2.1.7 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
