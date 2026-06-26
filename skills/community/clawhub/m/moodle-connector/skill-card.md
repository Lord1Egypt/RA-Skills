## Description: <br>
Moodle REST API client, batch downloader, and MCP server for Claude Code integration with SSO support for Azure AD, Google, and SAML. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jabir-srj](https://clawhub.ai/user/jabir-srj) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers, students, and education-technology operators use this skill to connect agents and command-line workflows to Moodle for course, grade, assignment, announcement, material, summary, and file-download tasks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles account tokens and private Moodle course data. <br>
Mitigation: Use only with trusted local MCP clients, protect config.json and credentials.enc, and exclude credentials, cache, and downloads from commits and backups. <br>
Risk: Download and write behavior can place files in user-selected output directories. <br>
Mitigation: Restrict downloads to trusted Moodle URLs and safe output directories, and review downloaded files before using or sharing them. <br>
Risk: Credential behavior is inconsistent in the release evidence, including a hardcoded test-pass path. <br>
Mitigation: Avoid the hardcoded test-pass path and require a strong MOODLE_CRED_PASSWORD or equivalent secret handling before deployment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jabir-srj/moodle-connector) <br>
- [Project homepage](https://github.com/Jabir-Srj/moodle-connector) <br>
- [Project repository](https://github.com/Jabir-Srj/moodle-connector.git) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, code, guidance] <br>
**Output Format:** [Markdown, command output, downloaded files, and MCP tool responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May read Moodle API data, cache responses, store encrypted credentials, and write downloaded files to configured directories.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release evidence and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
