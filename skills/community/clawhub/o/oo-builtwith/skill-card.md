## Description: <br>
BuiltWith. Use this skill for ANY BuiltWith request - searching and reading data. Whenever a task involves BuiltWith, use this skill instead of calling the API directly. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to retrieve BuiltWith technology intelligence for domains through an OOMOL-connected BuiltWith account, including domain profiles, summaries, recommendations, redirect history, and social-profile domain matches. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a connected BuiltWith account and uses OOMOL as an intermediary for access. <br>
Mitigation: Connect only the BuiltWith account and scopes intended for this skill, and rely on the connector flow instead of exposing raw tokens to the agent. <br>
Risk: First-time setup may involve piping a remote installer into a shell. <br>
Mitigation: Review the official oo CLI installation guide or installer before running the install command. <br>


## Reference(s): <br>
- [BuiltWith skill on ClawHub](https://clawhub.ai/oomol/oo-builtwith) <br>
- [oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [oo CLI installation guide](https://cli.oomol.com/install-guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON payload examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Connector responses are returned as JSON containing data and metadata, including an execution ID.] <br>

## Skill Version(s): <br>
1.0.1 (source: ClawHub release metadata and skill metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
