## Description: <br>
Runs a comprehensive 11-section health check on local OpenClaw installations, diagnosing configuration errors, session bloat, model drift, cron issues, security misconfigurations, gateway problems, and system instruction token budget. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bryant24hao](https://clawhub.ai/user/bryant24hao) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw operators use this skill to audit local OpenClaw installations, generate a prioritized diagnostic report, and apply approved repairs to configuration, session, cron, gateway, resource, and system-instruction issues. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Approved fixes can change or delete local OpenClaw files. <br>
Mitigation: Review the diagnostic report before approving fixes, prefer one-by-one repairs for config, security, and session changes, and confirm CRITICAL changes individually. <br>
Risk: Diagnostic output may include local configuration, session, log, cron, and workspace information in the agent conversation. <br>
Mitigation: Inspect the generated report before sharing it and rely on the skill's secret-redaction behavior for tokens, API keys, and passwords. <br>
Risk: The demo SVG may load a third-party font when rendered in privacy-sensitive offline environments. <br>
Mitigation: Avoid rendering the demo SVG in such environments or review the asset behavior before use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/bryant24hao/oc-doctor) <br>
- [Publisher profile](https://clawhub.ai/user/bryant24hao) <br>
- [Project homepage](https://github.com/bryant24hao/oc-doctor) <br>
- [User story](docs/user-story.en.md) <br>
- [System instruction checker](scripts/sysinstruction-check.sh) <br>
- [jq documentation](https://jqlang.github.io/jq/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown diagnostic report with severity labels, tables, inline shell commands, and interactive repair prompts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports redact secrets and ask for confirmation before modifying local files.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
