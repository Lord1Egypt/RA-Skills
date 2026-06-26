## Description: <br>
Generate a portfolio-aware daily or on-demand risk analysis brief from public market data, company updates, earnings material, and macro context, then emit a host-consumable handoff for persistence. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[prashamshah115](https://clawhub.ai/user/prashamshah115) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to turn a portfolio, watchlist, or market theme into a concise public-markets risk brief with exposure mapping, scenario analysis, watchpoints, source traceability, and uncertainty notes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Live retrieval can use an Apify token to create, update, or delete remote scraping tasks. <br>
Mitigation: Review the Apify bootstrap flow before enabling live providers, prefer manual task IDs when appropriate, and scope the Apify account used for the skill. <br>
Risk: Portfolio or watchlist-derived queries may be sent to Apify-backed Google or X scrapers. <br>
Mitigation: Avoid sensitive portfolio details, disable X signals when they are not needed, and use fixture or inline-only flows when external retrieval is inappropriate. <br>
Risk: Briefs, metadata, and portfolio context can be persisted locally or handed off for Notion storage. <br>
Mitigation: Avoid LOCAL_STATE_DIR unless local persistence is intended, and use inline delivery unless Notion storage is explicitly desired. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/prashamshah115/portfolio-risk-desk) <br>
- [Publisher Profile](https://clawhub.ai/user/prashamshah115) <br>
- [README](artifact/README.md) <br>
- [Skill Definition](artifact/SKILL.md) <br>
- [Tool Contract](artifact/intelligence_desk_brief_tool_contract.json) <br>
- [Output Template](artifact/intelligence_desk_brief_output_template.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Configuration, Guidance] <br>
**Output Format:** [Structured Markdown brief with JSON payloads and host handoff metadata] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Briefs include source traceability, audit metadata, confidence levels, uncertainty notes, and optional delivery handoff data.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
