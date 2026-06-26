## Description: <br>
Generates a daily Markdown financial briefing from China A-share market data and aggregated RSS news. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[answeryl](https://clawhub.ai/user/answeryl) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Users who follow China A-share markets and global news can run or schedule this skill to create a concise daily briefing with market index data, categorized headlines, summaries, and source links. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill fetches public market and news data, so source outages or stale feeds can affect briefing accuracy. <br>
Mitigation: Review the generated briefing and follow source links before using it for decisions. <br>
Risk: The skill can be scheduled to perform recurring network fetches and creates Markdown files in the configured Desktop output directory. <br>
Mitigation: Enable scheduling only when recurring runs are desired, and review or change the output directory if local retention matters. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/answeryl/global-market-briefing) <br>
- [Declared homepage](https://clawhub.com/skills/global-market-briefing) <br>
- [China News RSS](https://www.chinanews.com.cn/rss/) <br>
- [Tencent market quote endpoint](http://qt.gtimg.cn/q=sh000001,sz399001,sz399006,sh000688,sh000016) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Text, Files] <br>
**Output Format:** [Markdown briefing saved to a local file with a shorter text briefing printed to stdout] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes categorized headlines, source links, China A-share index data, and timestamps.] <br>

## Skill Version(s): <br>
1.0.1 (source: ClawHub release metadata; artifact frontmatter says 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
