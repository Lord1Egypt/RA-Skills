## Description: <br>
Office Automation Toolkit is a registry of CLI tools and Python packages for automating Excel, CSV, Word, PowerPoint, PDF, browser, network, and messaging workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[andyrenxu7255](https://clawhub.ai/user/andyrenxu7255) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and office automation users use this skill to choose appropriate tools and installation commands for document conversion, spreadsheet processing, PDF handling, browser automation, and messaging integrations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The bootstrap script can install packages and system tools, changing the host environment. <br>
Mitigation: Run scripts/toolkit-bootstrap.sh with --check-only first, review the planned changes, and prefer a virtual environment or container before allowing installation. <br>
Risk: The skill can bind Feishu lark-cli to Hermes credentials when matching environment variables are present. <br>
Mitigation: Allow credential binding only when those credentials are intentional, approved, and least-privileged for the task. <br>
Risk: Browser automation workflows may save reusable browser auth.json sessions for later headless use. <br>
Mitigation: Avoid saving reusable browser sessions for sensitive accounts, or store them with the same controls used for other account credentials. <br>


## Reference(s): <br>
- [Office Automation Tool Quick Reference](references/tool-quick-reference.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown with tool tables and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes a bootstrap shell script for checking or installing recommended office automation dependencies.] <br>

## Skill Version(s): <br>
1.1.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
