## Description: <br>
This skill helps agents prepare and publish video or text content across Douyin, Xiaohongshu, WeChat Channels, Bilibili, Weibo, and similar platforms with platform-specific adaptation, SEO tags, scheduling guidance, and publication status reporting. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tujinsama](https://clawhub.ai/user/tujinsama) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Content operators, marketers, and developers use this skill to adapt a content package for multiple social platforms, run the provided publishing flow, and review publication statuses and links. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Approved actions may publish content publicly or modify logged-in social media accounts. <br>
Mitigation: Review the exact accounts, platforms, content, and schedule before approval; test with drafts or a single account before broad distribution. <br>
Risk: Publishing credentials or API keys could expose social accounts if handled carelessly. <br>
Mitigation: Keep required secrets such as PUSH_API_KEY in local environment or secret files and do not commit or paste them into shared logs. <br>
Risk: Automation-backed platform publishing can be less stable on services without official APIs. <br>
Mitigation: Check the generated status report and links after each run, and manually verify failed, pending, or review-state posts. <br>


## Reference(s): <br>
- [Platform Rules](references/platform-rules.md) <br>
- [SEO Optimization](references/seo-optimization.md) <br>
- [Best Posting Time](references/best-posting-time.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, Text, Files] <br>
**Output Format:** [Markdown guidance with bash commands; the publishing script prints text status and writes a JSON publication record.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires pre-configured platform accounts; publishing can be immediate or scheduled and failed attempts are retried up to 3 times.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
