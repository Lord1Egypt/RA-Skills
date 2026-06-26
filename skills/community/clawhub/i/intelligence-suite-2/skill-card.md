## Description: <br>
Makima's All-Seeing Intelligence Suite combines real-time AI news tracking and global news monitoring for comprehensive strategic briefings with LLM analysis powered by SkillBoss API Hub. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[marjoriebroad](https://clawhub.ai/user/marjoriebroad) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to collect recent AI and global news signals, scrape article snippets, and generate structured strategic briefings through an external LLM service. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends scraped briefing content and SKILLBOSS_API_KEY-bearing requests to an undeclared external API domain. <br>
Mitigation: Confirm that api.heybossai.com is the intended SkillBoss endpoint before installing or providing SKILLBOSS_API_KEY. <br>
Risk: Global monitor output may mix one hardcoded mock news item into live analysis. <br>
Mitigation: Treat generated global-monitor briefings as unverified and review source items before relying on conclusions. <br>
Risk: Scraped article snippets are sent to an external LLM service for analysis. <br>
Mitigation: Avoid processing sensitive or private sources and review organizational data-sharing requirements before use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/marjoriebroad/intelligence-suite-2) <br>
- [Publisher profile](https://clawhub.ai/user/marjoriebroad) <br>
- [SkillBoss skill page](https://skillboss.co/skills/intelligence-suite) <br>
- [SkillBoss API endpoint declared in metadata](https://api.skillboss.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Console text containing structured news packs and LLM-generated briefing sections] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires node, npm, network access to configured news sources, and SKILLBOSS_API_KEY for LLM analysis.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
