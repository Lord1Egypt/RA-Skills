## Description: <br>
Scans local repositories with Mobb MCP/CLI and helps remediate reported security vulnerabilities with user-approved fixes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jonathansantilli](https://clawhub.ai/user/jonathansantilli) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and security engineers use this skill to scan a local code repository, review Mobb-proposed vulnerability fixes, and apply approved patches. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Monitoring checks can trigger scans and automatic code changes when auto-fix is enabled. <br>
Mitigation: Use only a trusted Mobb MCP server, keep auto-fix disabled unless intentional, and review local diffs before committing changes. <br>
Risk: Repository scans and remediation rely on Mobb authentication and may expose local repository context to the configured service. <br>
Mitigation: Use a scoped API key, confirm the target repository path before scanning, and authenticate only against the intended Mobb tenant. <br>


## Reference(s): <br>
- [MCP Tools for Mobb Fixes](references/mcp-scan-fix.md) <br>
- [Mobb Authentication and Login Flow](references/mobb-auth.md) <br>
- [ClawHub skill page](https://clawhub.ai/jonathansantilli/mobb-vulnerabilities-fixer) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, code, configuration] <br>
**Output Format:** [Markdown with inline commands and patch summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires explicit user consent before applying returned fixes.] <br>

## Skill Version(s): <br>
0.1.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
