## Description: <br>
Searches locally captured World Monitor data for news, earthquakes, Iran and Middle East events, technology, finance, layoffs, and keyword queries with bilingual English/Chinese presentation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oscarka](https://clawhub.ai/user/oscarka) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Agents and researchers use this skill to fetch public World Monitor-style data into a local cache and search recent news or OSINT-oriented topics by keyword and time window. It is useful for quick situational summaries around Iran, earthquakes, technology, finance, layoffs, and related events. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Fetch commands make outbound network requests and store a local searchable cache. <br>
Mitigation: Run fetch or update commands intentionally and review the configured local data directory before deployment. <br>
Risk: Telegram, Polymarket, OSINT, and news results may be incomplete, stale, or unverified. <br>
Mitigation: Treat retrieved items as source material for review, not as confirmed facts; verify important claims against authoritative sources. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/oscarka/intel-search) <br>
- [Publisher profile](https://clawhub.ai/user/oscarka) <br>
- [World Monitor](https://worldmonitor.app) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown-style terminal text with links, topic sections, and LANG hints] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports English and Chinese presentation, keyword or topic queries, and optional time windows such as 30min, 3h, 2d, and 1w.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata, artifact/clawhub.json, and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
