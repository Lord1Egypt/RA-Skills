## Description: <br>
Privacy-first UX research ethnography for OpenClaw that observes local usage over time, extracts local session data and conversations, analyzes workflow friction, and generates daily local-only reports with metrics, insights, anonymized evidence, and next-day research plans. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[giulianomorse](https://clawhub.ai/user/giulianomorse) <br>

### License/Terms of Use: <br>


## Use Case: <br>
OpenClaw users and teams use this skill to run local UX research on agent sessions, identify behavioral friction, and produce daily reports with redacted evidence, recommendations, and next-day research plans. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can read and retain OpenClaw conversation histories more broadly than its consent prompt clearly states. <br>
Mitigation: Use this_session_only and minimal or snippets capture unless broader collection is explicitly needed, review generated reports before sharing them, and use purge or a short retention window for sensitive work. <br>
Risk: Local reports and data files may contain sensitive conversation context even after redaction. <br>
Mitigation: Keep all artifacts local, apply the bundled redaction rules before persistence, and delete retained data with purge or purge full when no longer needed. <br>


## Reference(s): <br>
- [Fallback Session Paths](references/fallback-session-paths.md) <br>
- [Redaction Rules](references/redaction-rules.md) <br>
- [Report Template](references/report-template.md) <br>
- [Summary Schema](references/summary-schema.json) <br>
- [OpenClaw Creating Skills](https://docs.openclaw.ai/tools/creating-skills) <br>
- [OpenClaw Skills](https://docs.openclaw.ai/tools/skills) <br>
- [OpenClaw Skills Config](https://docs.openclaw.ai/tools/skills-config) <br>
- [OpenClaw Cron Jobs](https://docs.openclaw.ai/tools/cron-jobs) <br>
- [OpenClaw Session Management](https://docs.openclaw.ai/tools/session-management) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Files, Guidance] <br>
**Output Format:** [Chat summary plus local Markdown report and JSON summary files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports include redacted evidence, metrics, pain points, recommendations, saved file paths, and a next-day research plan.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
