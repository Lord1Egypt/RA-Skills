## Description: <br>
Cek harga emas Indonesia real-time (Antam/Logam Mulia), bandingkan brand, set alert harga, analisis AI via Kimi. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rhaone21](https://clawhub.ai/user/rhaone21) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and OpenClaw operators use this skill to check Indonesian gold prices, compare supported brands, manage price alerts, receive scheduled updates, track portfolio/history, and request Kimi-powered analysis when configured. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The setup guide requests broad OpenClaw permissions such as exec, group:fs, and a coding tool profile. <br>
Mitigation: Grant only the permissions needed to run the Node scripts and avoid broad filesystem or coding-profile access unless the deployment explicitly requires it. <br>
Risk: Scheduled alert and morning-brief jobs can send messages through Telegram or other announcement channels. <br>
Mitigation: Enable cron announcements only in private channels you control, and review cron messages before enabling scheduled delivery. <br>
Risk: AI analysis requires KIMI_API_KEY. <br>
Mitigation: Store KIMI_API_KEY as a secret or environment variable and avoid exposing it in logs, prompts, or shared configuration. <br>
Risk: Gold prices are scraped from external sources and may be stale or unavailable when a source changes or blocks access. <br>
Mitigation: Display scrape time and cache status to users, and verify prices against authoritative sources before making financial decisions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/rhaone21/id-emas-pro) <br>
- [API Sources for Gold Prices](references/api-sources.md) <br>
- [Antam Logam Mulia gold price source](https://www.logammulia.com/id/harga-emas-hari-ini) <br>
- [Pegadaian gold price source](https://www.pegadaian.co.id/harga-emas) <br>
- [Moonshot Kimi API platform](https://platform.moonshot.cn) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Indonesian plain text or Markdown with price tables, alert messages, analysis summaries, and setup command snippets.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May use local JSON files for alerts, cache, history, and portfolio data; AI analysis requires KIMI_API_KEY.] <br>

## Skill Version(s): <br>
1.3.0 (source: server release metadata and _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
