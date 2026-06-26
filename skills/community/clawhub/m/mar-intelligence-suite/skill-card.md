## Description: <br>
Makima's All-Seeing Intelligence Suite. Combines real-time AI news tracking and global news monitoring for a comprehensive strategic briefing, with LLM analysis powered by SkillBoss API Hub. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[marjoriebroad](https://clawhub.ai/user/marjoriebroad) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and agent users use this skill to run AI-news and global-news monitors that fetch recent public sources, scrape article snippets, and return strategic briefings. It is intended for agent-assisted intelligence summaries rather than a verified news or compliance workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends scraped article snippets and SKILLBOSS_API_KEY-authenticated requests to an external LLM endpoint. <br>
Mitigation: Use only with sources and API endpoints the installer trusts; avoid processing sensitive or confidential content unless the data-sharing path is approved. <br>
Risk: The declared network permissions mention api.skillboss.com, while the scripts call api.heybossai.com. <br>
Mitigation: Confirm the actual API host and update the declared permissions before deployment. <br>
Risk: The global monitor can include a fabricated placeholder entertainment item in briefings. <br>
Mitigation: Remove or clearly label mock data before relying on monitor output for decision-making. <br>
Risk: News and scraped snippets can be incomplete, unavailable, stale, or misleading. <br>
Mitigation: Treat generated briefings as leads for review and verify important claims against primary sources. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/marjoriebroad/mar-intelligence-suite) <br>
- [Publisher profile](https://clawhub.ai/user/marjoriebroad) <br>
- [SkillBoss Intelligence Suite listing](https://skillboss.co/skills/intelligence-suite) <br>
- [SkillBoss API Hub endpoint](https://api.heybossai.com/v1) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Plain text terminal output with structured news packs and generated briefing sections] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires SKILLBOSS_API_KEY for LLM analysis; without it, the scripts print fetched source material and skip model analysis.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
