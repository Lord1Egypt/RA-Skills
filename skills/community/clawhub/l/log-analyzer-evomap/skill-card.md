## Description: <br>
Analyzes error logs to extract structured exception details, classify common failure categories, identify file paths, derive prevention suggestions, and summarize batches of logs including EvoMap evolver logs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ractoto](https://clawhub.ai/user/ractoto) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to inspect application and EvoMap evolver error logs, classify failures, and produce structured summaries with prevention guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Local evolver logs may contain sensitive operational data. <br>
Mitigation: Review and redact logs before analysis, and avoid running the evolver log mode on directories containing secrets or private user data. <br>
Risk: The bundled publishing command can use ambient EvoMap/OpenClaw credentials to upload source code and platform metadata. <br>
Mitigation: Do not run `solidify` or expose the exported function unless publication is intended; unset publishing credentials in environments used only for log analysis. <br>
Risk: Heuristic log classification and generated prevention guidance can be incomplete or misleading. <br>
Mitigation: Treat summaries as triage assistance and verify root cause and remediation steps against the original logs and system context. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/ractoto/log-analyzer-evomap) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, guidance] <br>
**Output Format:** [Structured JSON objects or Markdown/text summary reports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May read local log files from ~/evolver-memory when that function or CLI mode is used.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata, SKILL.md frontmatter, package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
