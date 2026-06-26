## Description: <br>
Helps agents generate guidance, configuration, code snippets, and shell commands for building an agent-readable Hugo blog. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Byron-McKeeby](https://clawhub.ai/user/Byron-McKeeby) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and site operators use this skill to set up a minimal Hugo blog with agent-readable HTML, RSS output, metadata, nginx configuration, and operational scripts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Deployment snippets include nginx configuration changes and a privileged reload command. <br>
Mitigation: Review the nginx configuration and run sudo or reload nginx only on the intended server after confirming the deployment impact. <br>
Risk: The skill includes a third-party Hugo theme dependency. <br>
Mitigation: Review the theme source before use, as recommended by the server-provided security guidance. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Byron-McKeeby/hugo-blog-agent) <br>
- [Ananke Hugo theme](https://github.com/theNewDynamic/gohugo-theme-ananke) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash, TOML, HTML, XML, and nginx code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes deployment-oriented snippets that should be reviewed before execution.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
