## Description: <br>
Daily Chinese news brief from top global sources, with selectable categories and automated structured brief generation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Tkk0124](https://clawhub.ai/user/Tkk0124) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to fetch recent news from configured categories and generate concise Chinese daily briefs. It supports one-time setup, local configuration, optional scheduled execution, terminal preview, and saved text output. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: API keys may incur external service costs or be exposed if the generated .env file is shared. <br>
Mitigation: Use API keys with spending limits and keep the skill directory private when .env contains secrets. <br>
Risk: News queries, article metadata, and summarization prompts are sent to Serper and DeepSeek. <br>
Mitigation: Run the skill only when that third-party data sharing is acceptable for the selected news topics. <br>
Risk: Optional daily scheduling can repeatedly call paid APIs. <br>
Mitigation: Add the cron entry only when automatic daily execution is intended, and monitor usage. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/Tkk0124/news-brief) <br>
- [Serper News API Endpoint](https://serper.dev/news) <br>
- [DeepSeek Chat Completions Endpoint](https://api.deepseek.com/v1/chat/completions) <br>


## Skill Output: <br>
**Output Type(s):** [text, files, shell commands, configuration, guidance] <br>
**Output Format:** [Plain text Chinese news brief, terminal output, and dated .txt file output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Brief content depends on configured categories, time range, news count, Serper results, and DeepSeek summarization.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
