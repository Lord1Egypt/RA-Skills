## Description: <br>
Post-mortem analysis for AI agent failures. Capture state, reconstruct timelines, identify root causes. When your agent breaks, know what happened, why, and how to prevent it. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[TheShadowRose](https://clawhub.ai/user/TheShadowRose) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and operators use Incident Replay to capture local workspace snapshots around agent failures, reconstruct timelines, classify likely causes, and produce reports for manual remediation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill intentionally copies workspace file contents, logs, and decision traces into local incident data. <br>
Mitigation: Set WORKSPACE_ROOT narrowly, exclude secrets and private directories, and keep generated incident_data outside synced or shared folders. <br>
Risk: Generated reports and snapshots may contain sensitive local workspace context. <br>
Mitigation: Review generated Markdown, JSON, and snapshot files before sharing or committing them. <br>
Risk: Untrusted or path-like output values can direct report files to unintended locations. <br>
Mitigation: Use controlled local output paths and avoid accepting report output paths from untrusted sources. <br>
Risk: Root cause classification is heuristic and may confuse correlation with causation. <br>
Mitigation: Treat findings as investigative guidance and require human review before remediation. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/TheShadowRose/incident-replay) <br>
- [Publisher profile](https://clawhub.ai/user/TheShadowRose) <br>
- [README.md](artifact/README.md) <br>
- [LIMITATIONS.md](artifact/LIMITATIONS.md) <br>
- [OpenClaw project](https://github.com/openclaw/openclaw) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown reports, JSON records, terminal text, and local workspace snapshot files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses local configuration and writes snapshots, incidents, and reports under the configured data directory.] <br>

## Skill Version(s): <br>
1.0.6 (source: server release metadata; artifact frontmatter remains 1.0.5) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
