## Description: <br>
A lightweight Google Workspace command-line helper for Gmail, Calendar, and Drive operations for personal daily use. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Personal users, developers, and command-line oriented workers use this skill to have an agent prepare or run gog CLI commands for searching and reading Gmail, sending plain-text email, querying Google Calendar events, and searching Google Drive files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide an agent to use OAuth-backed Gmail, Calendar, and Drive access, including sending email and using locally stored credentials. <br>
Mitigation: Review the skill before installation, use only an intended Google account and OAuth client, verify where gog stores credentials, and require explicit confirmation before sending email or running no-input/scripted commands. <br>
Risk: The security scan reports overbroad and unrelated trigger language, including SEO terms, which can expand when the skill activates. <br>
Mitigation: Narrow activation and trigger language to Google Workspace operations before broad deployment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thcjp/skills/google-workspace-cli-free) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and examples; command output may be text, JSON, or CSV depending on gog options.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a Google OAuth client, a configured gog CLI, network access to Google APIs, and an agent allowed to read files and execute shell commands.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
