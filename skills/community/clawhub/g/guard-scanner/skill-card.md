## Description: <br>
Security scanner and runtime guard for OpenClaw skills, MCP servers, and AI agent workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[koatora20](https://clawhub.ai/user/koatora20) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and security reviewers use this skill to scan agent skills, MCP servers, and OpenClaw workspaces before install or deployment, generate JSON/SARIF/HTML reports for CI, audit public assets for credential exposure, and enforce before_tool_call policy in OpenClaw. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release evidence marks the security verdict as suspicious because the metadata and security claims understate network, environment, shell, MCP, and persistent runtime behavior. <br>
Mitigation: Install only after reviewing the scanner's requested authority, run audit/crawl/patrol/serve modes in controlled environments, and document the local state paths it writes before enabling runtime enforcement. <br>
Risk: The skill can load custom rules or plugin files and may scan broad local workspaces. <br>
Mitigation: Avoid untrusted --plugin or custom rules files, limit scan targets to intended directories, and run scans with least-privilege filesystem and network access. <br>
Risk: Runtime guard and MCP server modes can affect tool-call flow and expose scanner tools to connected agents. <br>
Mitigation: Use monitor mode first, review audit logs, and enable enforce or strict mode only after validating expected findings and false-positive impact. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/koatora20/guard-scanner) <br>
- [SKILL.md](artifact/SKILL.md) <br>
- [OpenClaw plugin manifest](artifact/openclaw.plugin.json) <br>
- [Threat Taxonomy](artifact/docs/THREAT_TAXONOMY.md) <br>
- [Evidence-Driven Metrics](artifact/docs/EVIDENCE_DRIVEN.md) <br>
- [Threat Model](artifact/docs/threat-model.md) <br>
- [Capabilities specification](artifact/docs/spec/capabilities.json) <br>
- [npm package](https://www.npmjs.com/package/@guava-parity/guard-scanner) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance plus JSON, SARIF, HTML, CLI output, MCP tool responses, and OpenClaw runtime guard decisions.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires node; may write audit and task state under ~/.openclaw/guard-scanner when runtime guard, audit, crawl, patrol, or serve modes are used.] <br>

## Skill Version(s): <br>
16.0.2 (source: server release evidence, package.json, openclaw.plugin.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
