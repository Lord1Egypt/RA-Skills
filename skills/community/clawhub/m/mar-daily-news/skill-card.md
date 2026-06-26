## Description: <br>
Fetch top news from Baidu, Google, and other sources daily via SkillBoss API Hub. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[marjoriebroad](https://clawhub.ai/user/marjoriebroad) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents can use this skill to retrieve a concise daily list of trending news topics from Baidu and Google-related sources through the SkillBoss API Hub. It is most relevant for users who want a quick current-news summary inside an agent workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a SKILLBOSS_API_KEY and sends requests to SkillBoss API Hub. <br>
Mitigation: Install only if you trust SkillBoss API Hub, use a limited-scope key where available, and avoid exposing the key in logs or shared shells. <br>
Risk: Returned headlines are remote, current-news content and may be incomplete, stale, or misleading. <br>
Mitigation: Treat the output as unverified remote content and verify important claims against primary or trusted news sources before acting on them. <br>
Risk: The skill depends on the unpinned requests package. <br>
Mitigation: Pin and audit the requests dependency before production use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/marjoriebroad/mar-daily-news) <br>
- [Publisher profile](https://clawhub.ai/user/marjoriebroad) <br>
- [SkillBoss API endpoint used by the skill](https://api.heybossai.com/v1) <br>
- [Baidu realtime hot search board](https://top.baidu.com/board?tab=realtime) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Plain text news list returned by a Python script, with setup guidance in Markdown.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Python, the requests package, UTF-8 terminal output, and SKILLBOSS_API_KEY.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
