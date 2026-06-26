## Description: <br>
Fetch real-time AI news briefings powered by SkillBoss API Hub from sources such as Hacker News, TechCrunch, and The Verge, then summarize them for agent use. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[modestyrichards](https://clawhub.ai/user/modestyrichards) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to fetch current AI news and turn search results into concise briefings with timestamps and source links. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a SkillBoss API key and sends briefing requests to SkillBoss. <br>
Mitigation: Use a dedicated API key, store it as an environment variable, and avoid passing private prompts or sensitive context into briefing requests. <br>
Risk: Manual installation references may not match server-resolved provenance because provenance is unavailable for this version. <br>
Mitigation: Install from ClawHub or verify any repository and release contents before manual installation. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/modestyrichards/modesty-ai-news-oracle) <br>
- [SkillBoss setup guide](https://skillboss.co/skill.md) <br>
- [SkillBoss API endpoint](https://api.skillboss.co/v1/pilot) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Concise AI news briefing text or JSON-style summary with timestamps and source links] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires SKILLBOSS_API_KEY and external requests to SkillBoss.] <br>

## Skill Version(s): <br>
1.0.2 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
