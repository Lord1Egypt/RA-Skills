## Description: <br>
Fetches top Hacker News stories, translates titles to Chinese with Baidu Translate, writes a bilingual Markdown report, and can optionally post the report to Feishu. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[joewangup](https://clawhub.ai/user/joewangup) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators can use this skill to generate a daily bilingual Hacker News digest, with optional Feishu delivery for team visibility. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The script sends requests to Hacker News and Baidu Translate, and can send report content to Feishu when a webhook is configured. <br>
Mitigation: Run it only where those outbound requests are acceptable, use limited Baidu credentials, and set FEISHU_WEBHOOK only for intended destinations. <br>
Risk: The report path ~/daily-news.md is overwritten on each run. <br>
Mitigation: Move or rename reports that need to be retained before running the script again. <br>
Risk: A Feishu webhook URL can allow posting into the configured chat if exposed. <br>
Mitigation: Store the webhook as a protected environment variable and rotate it if it may have been disclosed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/joewangup/hacker-news-summary) <br>
- [Baidu Translate Open Platform](https://fanyi-api.baidu.com/) <br>
- [Hacker News Firebase API](https://hacker-news.firebaseio.com/v0/topstories.json) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, shell commands, configuration] <br>
**Output Format:** [Markdown report with bilingual news titles and links, plus optional text delivery to Feishu] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Baidu Translate credentials; optionally uses a Feishu webhook; writes the report to ~/daily-news.md.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence and SKILL.md) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
