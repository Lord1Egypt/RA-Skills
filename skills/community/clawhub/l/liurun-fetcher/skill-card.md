## Description: <br>
Automatically fetches Liu Run's latest WeChat public articles and generates structured summaries with key insights and trend judgments. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[coolfzb](https://clawhub.ai/user/coolfzb) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to trigger or schedule retrieval of Liu Run WeChat/Sogou articles, archive article material locally, and receive concise business-news summaries with insights and trend judgments. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad keyword triggers or schedules may fetch and store article material locally when the user did not intend a run. <br>
Mitigation: Confirm before enabling cron schedules or broad triggers, and review saved files in the articles folder. <br>
Risk: Personalized financial holdings context may be included in generated summaries and saved locally. <br>
Mitigation: Avoid providing portfolio or Trade Arena data unless it is intended for local storage, or redact it before summary generation. <br>
Risk: Automated WeChat/Sogou browsing may depend on a logged-in browser profile and external anti-scraping behavior. <br>
Mitigation: Use a dedicated browser profile where possible, respect site access limits, and review fetched content before relying on it. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/coolfzb/liurun-fetcher) <br>
- [Skill source overview](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Files, Shell commands, Guidance] <br>
**Output Format:** [Markdown summaries plus saved article and raw text files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May save article summaries, raw article text, and debug HTML under the articles folder.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
