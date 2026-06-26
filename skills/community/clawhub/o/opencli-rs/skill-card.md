## Description: <br>
Opencli Rs helps agents use OpenCLI-style command workflows to automate supported websites, desktop applications, local CLI tools, data collection, and content downloads. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[smallnest](https://clawhub.ai/user/smallnest) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to discover and run command-line automations for web platforms, Electron desktop applications, external CLIs, structured data collection, and content download workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can enable broad browser, account, desktop application, and local CLI actions. <br>
Mitigation: Use a dedicated browser profile or test accounts, restrict allowed commands, and require explicit approval before posting, deleting, messaging, following, blocking, bulk downloading, sending local files or code, or invoking developer and infrastructure CLIs. <br>
Risk: Installation provenance and version drift need review before use. <br>
Mitigation: Review the package before installation and pin and verify the package or binary instead of using latest-version or curl-to-shell installation flows. <br>
Risk: Auto-update and keep-alive behavior can extend the authority of the browser or local automation environment. <br>
Mitigation: Disable auto-update and keep-alive behavior unless needed, and monitor the browser profile, daemon status, and installed plugins. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/smallnest/opencli-rs) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/smallnest) <br>
- [Artifact-referenced OpenCLI-RS project](https://github.com/nashsu/opencli-rs) <br>
- [Artifact-referenced OpenCLI project](https://github.com/jackwener/opencli) <br>
- [OpenClaw documentation](https://docs.openclaw.ai) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and example scripts; OpenCLI command results may be JSON, YAML, CSV, Markdown, or tables.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Some workflows write local configuration, reports, downloaded files, and structured data outputs.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
