## Description: <br>
Advanced text-based integration suite for Palantir Maven Smart System (MSS) target workflows, including target lookup, Kanban status updates, CDE risk checks, SIGINT context, asset assignment, logistics, weather, BDA reporting, and pattern-of-life analysis. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[freQuensy23-coder](https://clawhub.ai/user/freQuensy23-coder) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Authorized operators and supporting developers use this skill to translate text requests into Palantir MSS API calls and receive concise operational reports. It can also mutate strike workflow state, so deployments should restrict credentials and require human approval for target status changes or asset assignments. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill connects to a high-impact military targeting environment and can change strike workflow state. <br>
Mitigation: Install only for authorized MSS environments and require external human approval before target status changes, asset assignment, or any action that moves a target closer to engagement. <br>
Risk: The setup flow stores an MSS API key in a local .env file. <br>
Mitigation: Use least-privileged credentials, prefer read-only access unless mutation is required, protect file permissions, and delete or rotate credentials when no longer needed. <br>
Risk: Reports and downstream actions depend on data returned by the configured endpoint. <br>
Mitigation: Verify the publisher and endpoint before installation, and review returned target, CDE, SIGINT, weather, and deconfliction data before operational use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/freQuensy23-coder/palantir-integration) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, API calls] <br>
**Output Format:** [Structured text and Markdown reports with shell command-backed tool calls] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May read or write MSS state through configured API credentials and local environment configuration.] <br>

## Skill Version(s): <br>
1.0.1 (source: ClawHub release metadata; artifact frontmatter declares 2.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
