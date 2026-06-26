## Description: <br>
Fetches LightReading and TechCrunch news, prepares Chinese AI summaries, and sends the digest to Enterprise WeChat. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sophieliiiiii](https://clawhub.ai/user/sophieliiiiii) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators can use this skill to automate a Chinese technology-news digest from LightReading and TechCrunch. It supports scheduled collection, AI summarization, local summary files, and Enterprise WeChat delivery. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Hard-coded Enterprise WeChat webhook keys can expose or misuse the configured message destination. <br>
Mitigation: Remove embedded webhook keys before use, rotate any real key, and configure the destination through a secret or local configuration. <br>
Risk: Scheduled automation can send summaries at unintended times or to unintended channels. <br>
Mitigation: Verify the cron schedule and destination configuration before enabling recurring pushes. <br>
Risk: The optional email webhook server can create unsafe network exposure if run on a reachable interface. <br>
Mitigation: Bind it to localhost, add protection before network exposure, and remove the health-check directory listing if the server is kept. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/sophieliiiiii/lightreading-daily) <br>
- [LightReading RSS feed](https://www.lightreading.com/rss.xml) <br>
- [TechCrunch feed](https://techcrunch.com/feed/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Chinese digest text with Markdown-style links, plus setup commands and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes local English and Chinese summary files and can send text payloads to Enterprise WeChat.] <br>

## Skill Version(s): <br>
5.9.1 (source: server release metadata and SKILL.md version history) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
