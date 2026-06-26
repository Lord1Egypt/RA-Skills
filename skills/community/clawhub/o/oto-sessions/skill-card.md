## Description: <br>
Manage authenticated browser sessions for any website with Oto, enabling agents to save, list, delete, and automate multiple accounts without re-authenticating. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mbahar](https://clawhub.ai/user/mbahar) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and automation agents use this skill to save, reuse, inspect, delete, and launch authenticated browser sessions for websites and multiple account profiles. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Saved browser sessions can function like credentials for logged-in accounts. <br>
Mitigation: Use the skill only on a trusted, single-user machine and avoid banking, email, admin, or other high-value accounts unless the user fully accepts the risk. <br>
Risk: Session files, logs, or debug details may expose authenticated access if shared or committed. <br>
Mitigation: Do not share or commit saved session files or logs, keep session storage local, and delete saved sessions when they are no longer needed. <br>
Risk: Browser-control commands can act with the privileges of the saved account. <br>
Mitigation: Review commands and target accounts before execution, and prefer the least-privileged account appropriate for the task. <br>


## Reference(s): <br>
- [Setup Guide](references/SETUP.md) <br>
- [Integration Guide](references/INTEGRATION.md) <br>
- [Oto Framework Repository](https://github.com/mbahar/oto) <br>
- [Playwright Documentation](https://playwright.dev) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, JSON] <br>
**Output Format:** [Markdown documentation with shell commands, JavaScript snippets, and JSON CLI output.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Some wrappers return process exit codes and session metadata for automation workflows.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
