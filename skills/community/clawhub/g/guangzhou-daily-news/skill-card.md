## Description: <br>
Fetches the latest Guangzhou Daily/Xinhuacheng news, extracts titles, summaries, source links, editor and reporter details, and formats the results as Markdown with optional scheduled or WeChat-style delivery. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[FreeEye](https://clawhub.ai/user/FreeEye) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Readers and agents use this skill to collect Guangzhou local news from Guangzhou Daily/Xinhuacheng on demand or on a daily schedule, then produce a concise digest for reading or sharing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Scheduled delivery may send recurring news updates without a fresh manual action. <br>
Mitigation: Review OpenClaw cron entries and any separate WeChat integration before authorizing recurring pushes or account access. <br>
Risk: The skill writes generated Markdown files to the local ~/News directory. <br>
Mitigation: Confirm the output location is acceptable and adjust or disable scheduled runs if automatic local file creation is not desired. <br>
Risk: News summaries and attribution depend on content fetched from Guangzhou Daily/Xinhuacheng pages and may be incomplete when page structure changes. <br>
Mitigation: Check the source links in the digest before relying on or sharing time-sensitive news details. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/FreeEye/guangzhou-daily-news) <br>
- [Guangzhou Daily Xinhuacheng main site](https://gz-cmc.com) <br>
- [Xinhuacheng mobile site](https://huacheng.gz-cmc.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown digest and short text message summary] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes Markdown files under ~/News and can produce a WeChat-style summary message.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
