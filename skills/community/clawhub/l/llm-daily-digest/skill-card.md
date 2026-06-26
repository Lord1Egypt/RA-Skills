## Description: <br>
生成中文 LLM / 大模型每日简报，采集头部厂商官方博客、GitHub Trending、arXiv、Hugging Face、Papers With Code、Hacker News、X/Twitter 和中文媒体，筛选去重后保存结构化 Markdown 报告。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[flowbywind](https://clawhub.ai/user/flowbywind) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and AI practitioners use this skill to generate a daily Chinese digest of LLM news, model releases, papers, open-source projects, and industry events. It is intended for manual prompts or scheduled OpenClaw runs that produce a dated local report and a short session summary. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill creates dated Markdown digest files in the OpenClaw workspace, which may be shared or synced in some environments. <br>
Mitigation: Install only where local digest files are expected, and periodically review or clean old reports in shared workspaces. <br>
Risk: Broad natural-language activation phrases and scheduled runs can overlap with other news or summary skills. <br>
Mitigation: Use an explicit prompt or the llm-daily-digest skill name for scheduled runs. <br>
Risk: The digest depends on external news, repository, paper, and social sources that may be unavailable or incomplete during a run. <br>
Mitigation: Treat the report as a convenience summary, review important items against source links, and preserve collection statistics or coverage notes. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/flowbywind/llm-daily-digest) <br>
- [OpenClaw skills documentation](https://docs.openclaw.ai/tools/skills) <br>
- [OpenClaw cron jobs documentation](https://docs.openclaw.ai/automation/cron-jobs) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Files, Text] <br>
**Output Format:** [Structured Chinese Markdown report plus a short chat response with file path, top picks, and collection statistics.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Saves dated digest files under ~/.openclaw/workspace/digests and avoids overwriting existing reports by adding version suffixes.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
