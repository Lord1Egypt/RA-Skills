## Description:

Summarizes URLs, local files, and YouTube links through OpenAI-compatible Chinese model APIs such as Qianfan, DashScope, Hunyuan, Volcano Engine, Moonshot, and DeepSeek.

This skill is ready for commercial/non-commercial use.

## Publisher:

[43622283](https://clawhub.ai/user/43622283)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and knowledge workers use this skill to configure and run the summarize CLI for web pages, local documents, and YouTube videos using OpenAI-compatible model providers, especially China-hosted providers.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Input content and summaries may be sent to third-party model APIs.

Mitigation: Avoid confidential local files or private videos unless the configured provider is trusted, or use a local endpoint such as Ollama.

Risk: The installer can install an unpinned global npm package.

Mitigation: Review the package before installation and prefer a pinned or local install of the summarize CLI.

Risk: API keys may be stored in the user's summarize configuration file.

Mitigation: Prefer environment variables for secrets, and restrict ~/.summarize to chmod 700 and ~/.summarize/config.json to chmod 600 if keys are stored there.

Risk: Setup scripts write configuration under the user's home directory.

Mitigation: Do not run the installer as root, and review generated configuration before using it with real data.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/43622283/skills/li-summarize)
- [ClawHub Publisher Profile](https://clawhub.ai/user/43622283)
- [summarize CLI](https://summarize.sh)
- [Baidu QianFan](https://cloud.baidu.com/product/wenxinworkshop)
- [Alibaba DashScope](https://dashscope.aliyuncs.com/)
- [Tencent Hunyuan](https://cloud.tencent.com/product/hunyuan)
- [DeepSeek Platform](https://platform.deepseek.com/)
- [Zhipu AI](https://open.bigmodel.cn/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can guide JSON output from the underlying summarize CLI when requested by the user.]

## Skill Version(s):

0.0.2 (source: server release evidence; artifact frontmatter says 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
