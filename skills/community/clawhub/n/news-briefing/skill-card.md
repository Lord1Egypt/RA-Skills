## Description: <br>
Creates real-time Chinese-language news briefings for any topic by searching the web, summarizing top stories, and delivering a Feishu card with optional AI insights. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[derekhsu529](https://clawhub.ai/user/derekhsu529) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users, employees, and developers use this skill to request topical news briefings and receive concise Chinese summaries with source links and optional AI insight sections in Feishu. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: User-supplied topics or titles are placed into shell command strings while API and Feishu credentials are available. <br>
Mitigation: Review before installation, do not let untrusted text become a topic or title, and replace shell-string execSync calls with spawn or execFile argument arrays or native fetch calls before routine use. <br>
Risk: The skill can send Feishu messages using real tenant credentials. <br>
Mitigation: Use least-privilege Feishu credentials, configure target recipients deliberately, and enable cron only for reviewed briefing topics. <br>
Risk: News requests may include sensitive topics and are sent to third-party APIs. <br>
Mitigation: Avoid sensitive topics and review organizational data-handling requirements before providing API keys. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/derekhsu529/news-briefing) <br>
- [Publisher profile](https://clawhub.ai/user/derekhsu529) <br>
- [Perplexity chat completions API](https://api.perplexity.ai/chat/completions) <br>
- [PPIO OpenAI-compatible chat completions API](https://api.ppinfra.com/v3/openai/chat/completions) <br>
- [Feishu tenant access token API](https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal) <br>
- [Feishu message send API](https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type=open_id) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, configuration] <br>
**Output Format:** [Chinese-language summaries and Feishu interactive-card JSON, with Markdown sections and source links.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Feishu app credentials and a Perplexity API key; an optional PPIO API key enables AI insight sections.] <br>

## Skill Version(s): <br>
2.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
