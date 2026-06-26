## Description: <br>
Use the Privacy CLI to create and manage Privacy Virtual Cards directly from the terminal. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[eladrave](https://clawhub.ai/user/eladrave) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to let an agent propose and run Privacy.com CLI commands for virtual card lifecycle tasks and transaction lookup. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can create, update, pause, unpause, reveal details for, or permanently close financial virtual cards. <br>
Mitigation: Require explicit user confirmation before each card-changing or PAN-revealing command, and verify the exact card token or memo before running it. <br>
Risk: The Privacy API key grants access to sensitive card and transaction data. <br>
Mitigation: Keep PRIVACY_API_KEY out of files and logs, prefer environment-variable configuration, and avoid storing command output that contains sensitive card data. <br>
Risk: The skill may install or rely on a global npm CLI package. <br>
Mitigation: Have the user approve any global npm installation and confirm the installed privacy CLI before use. <br>


## Reference(s): <br>
- [Privacy CLI documentation](https://developers.privacy.com/docs/privacy-cli) <br>
- [ClawHub skill listing](https://clawhub.ai/eladrave/privacy-cli) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance, JSON] <br>
**Output Format:** [Markdown with inline shell commands and JSON CLI output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses non-interactive Privacy CLI commands with --json output.] <br>

## Skill Version(s): <br>
1.0.2 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
