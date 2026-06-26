## Description: <br>
Monitor Google AI Studio (Gemini API) usage, rate limits, and quota consumption with automated alerts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xiaoyaner0201](https://clawhub.ai/user/xiaoyaner0201) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to check Google AI Studio project usage, identify rate-limit or quota pressure, and send concise Discord alerts before usage reaches configured thresholds. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The agent may inspect or report usage for the wrong Google AI Studio project or account. <br>
Mitigation: Confirm the project ID and active Google account before opening the usage dashboard or enabling scheduled checks. <br>
Risk: Usage reports or alerts may be posted to an unintended Discord channel or on an unintended schedule. <br>
Mitigation: Use a private intended channel, verify the channel ID, and review cron and HEARTBEAT entries before automation is enabled. <br>


## Reference(s): <br>
- [Google AI Studio Usage Dashboard](https://aistudio.google.com/usage) <br>
- [Gemini API Rate Limits](https://ai.google.dev/gemini-api/docs/rate-limits) <br>
- [Gemini API Billing Documentation](https://ai.google.dev/gemini-api/docs/billing) <br>
- [Cloud Monitoring for Gemini](https://firebase.google.com/docs/ai-logic/monitoring) <br>
- [ClawHub Skill Page](https://clawhub.ai/xiaoyaner0201/google-ai-usage-monitor) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown reports with inline browser automation commands and JSON configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes usage thresholds, Discord report templates, alert wording, and optional cron and heartbeat setup guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: SKILL.md frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
