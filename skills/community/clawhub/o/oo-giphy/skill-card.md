## Description: <br>
GIPHY (giphy.com). Use this skill for ANY GIPHY request - searching and reading data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to search, fetch, translate, and inspect GIFs, stickers, categories, and tags through a connected GIPHY account. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a connected GIPHY account and uses OOMOL as an intermediary for GIPHY operations. <br>
Mitigation: Install only when that intermediary model is acceptable and connect the GIPHY API key or account through OOMOL intentionally. <br>
Risk: Optional first-time setup commands install or authenticate the oo CLI. <br>
Mitigation: Review the oo CLI installer separately and run setup commands only when the CLI, authentication, or connection is missing. <br>
Risk: Billing or credential issues can stop connector execution. <br>
Mitigation: Follow the documented recovery paths for expired credentials, missing scopes, missing app connections, or OOMOL billing errors before retrying. <br>


## Reference(s): <br>
- [GIPHY homepage](https://giphy.com) <br>
- [oo CLI](https://github.com/oomol-lab/oo-cli) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON payload examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Connector responses are returned as JSON data with execution metadata.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
