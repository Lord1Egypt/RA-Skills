## Description: <br>
Analyzes OpenClaw token usage and cost from local session logs, identifies high-cost patterns, and produces optimization recommendations and a Markdown cost report. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dagangtj](https://clawhub.ai/user/dagangtj) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to review local model usage, token volume, and estimated cost, then decide where to reduce context size, change model selection, or adjust recurring jobs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The generated cost report can expose sensitive local usage details such as model choices, session identifiers, token volumes, and cost patterns. <br>
Mitigation: Store and share the report as sensitive local data, and review it before moving it outside the OpenClaw workspace. <br>
Risk: Optimization guidance may include cleanup, model-change, or cron commands that affect future OpenClaw behavior. <br>
Mitigation: Review commands manually and run only the changes that match your intended workflow and retention policy. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dagangtj/openclaw-cost-analyzer) <br>
- [README](README.md) <br>
- [Security Policy](SECURITY.md) <br>
- [Changelog](CHANGELOG.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Console text and Markdown cost report with recommended shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reads local OpenClaw session logs and writes a local cost-analysis report.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter, package.json, CHANGELOG, server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
