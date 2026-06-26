## Description: <br>
OpenCLI provides command-line guidance for website access and browser automation across public APIs, logged-in browser sessions, and local CLI integrations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chensu1234](https://clawhub.ai/user/chensu1234) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to run opencli commands for website search, news, social feeds, browser interaction, screenshots, scraping, and selected external CLI tools. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide agents to use logged-in browser sessions, screenshots, form entry, clicks, chained operations, and automation that may affect account or local data. <br>
Mitigation: Use a separate low-risk browser profile and require explicit confirmation before logged-in commands, screenshots, form entry, clicks, chained operations, or data-changing actions. <br>
Risk: The skill may depend on a separate opencli executable and external CLI auto-install behavior. <br>
Mitigation: Install only when the opencli executable is trusted, and disable or require approval for automatic installs. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/chensu1234/opencli-hub) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands; opencli command output is structured text with optional JSON for supported commands.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May rely on a local opencli executable, Chrome session state, and external CLI tools.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
