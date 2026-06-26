## Description: <br>
Monitors Persian-language X activity related to Iran, ranks and translates high-signal posts, scores escalation risk, and produces Markdown intelligence reports with optional alerts and daily briefings. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ArthuronAI](https://clawhub.ai/user/ArthuronAI) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Journalists, OSINT teams, geopolitical analysts, and monitoring operations use this skill to track Persian-language Iran-related social signals, translate notable posts, and generate escalation-oriented briefings. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can send scan results to external alert channels and providers. <br>
Mitigation: Disable Telegram, Slack, and webhook alerts until destinations are reviewed, and only configure providers approved to receive the relevant scan data. <br>
Risk: Telegram credentials and chat destinations are configured in the skill settings. <br>
Mitigation: Keep bot tokens and chat IDs out of source-controlled configuration and inject them through a secure runtime secret mechanism. <br>
Risk: Daily briefing summaries may be static or stale if history and summarization behavior are not reviewed. <br>
Mitigation: Validate briefing output against recent scan history before using it for operational decisions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ArthuronAI/iran-intelligence-radar) <br>
- [Artifact README](artifact/README.md) <br>
- [Skill definition](artifact/SKILL.md) <br>
- [System prompt](artifact/prompts/system_prompt.md) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Markdown, API Calls, Configuration, Guidance] <br>
**Output Format:** [Markdown report plus structured scan result fields] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes ranked tweet rows, multilingual translations, escalation score and level, trending signals, alert status, billing state, and optional daily briefing.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
