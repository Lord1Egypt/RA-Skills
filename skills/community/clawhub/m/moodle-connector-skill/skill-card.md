## Description: <br>
Moodle REST API client, batch downloader, and MCP server for Claude Code integration. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jabir-srj](https://clawhub.ai/user/jabir-srj) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers, students, and LMS administrators use this skill to connect an agent or CLI workflow to Moodle for course data, grades, assignments, materials, downloads, deadlines, announcements, and markdown summaries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles Moodle tokens and credential passwords. <br>
Mitigation: Use a strong environment or secret-manager value for the credential password, remove test defaults before real use, and keep real tokens out of checked-in configuration files. <br>
Risk: The skill can download files and write cache data locally. <br>
Mitigation: Restrict downloads to the intended Moodle domain and use a dedicated downloads/cache directory with appropriate access controls. <br>
Risk: The MCP server exposes Moodle actions to the connected MCP client. <br>
Mitigation: Install only with a trusted MCP client and review requested tool calls before allowing access to sensitive Moodle data. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jabir-srj/moodle-connector-skill) <br>
- [Project homepage](https://github.com/Jabir-Srj/moodle-connector) <br>
- [Project repository](https://github.com/Jabir-Srj/moodle-connector.git) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, API Calls, Files, Shell commands, Configuration] <br>
**Output Format:** [Markdown, JSON configuration, CLI text, MCP tool responses, and downloaded files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Moodle credentials or token configuration; may write downloaded content and cache data to local directories.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata; package.json reports 1.0.6) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
