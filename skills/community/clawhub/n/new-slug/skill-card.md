## Description: <br>
Helps users discover and install agent skills when they ask questions like "how do I do X", "find a skill for X", "is there a skill that can...", or express interest in extending capabilities. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pipsqueakup](https://clawhub.ai/user/pipsqueakup) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to search for installable skills, compare relevant options, and produce install commands or links for skill packages that may fit a requested task. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may steer ordinary help requests toward third-party skill installation. <br>
Mitigation: Treat search results as suggestions and review the exact package, publisher, and purpose before installing anything. <br>
Risk: The skill recommends global no-confirmation installation commands. <br>
Mitigation: Prefer explicit user confirmation and avoid global no-confirm installs unless the user intentionally accepts that behavior. <br>
Risk: The included Python demo uses AgentScope with a DashScope API key. <br>
Mitigation: Do not run the demo unless AgentScope use and DashScope credential handling are intentional for the environment. <br>


## Reference(s): <br>
- [Artifact reference documentation](references/DOC.md) <br>
- [ClawHub release page](https://clawhub.ai/pipsqueakup/new-slug) <br>
- [Skills directory](https://skills.sh/) <br>
- [Claude Skills overview](https://claude.com/blog/skills) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands] <br>
**Output Format:** [Markdown with inline shell commands and links] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May reference external skill registries and user-approved install commands.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
