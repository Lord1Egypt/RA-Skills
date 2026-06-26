## Description: <br>
Li Summarize helps agents configure and use the summarize CLI with OpenAI-compatible Chinese model providers to summarize URLs, local files, and YouTube links. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[43622283](https://clawhub.ai/user/43622283) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users use this skill to install or configure the summarize CLI for OpenAI-compatible providers, especially Chinese model services. It supports summarizing web pages, local files, and YouTube links with provider-specific model and endpoint settings. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Summarized URLs, files, or YouTube content may be sent to the configured OpenAI-compatible model provider. <br>
Mitigation: Use only approved providers and avoid sensitive documents, private URLs, or regulated data unless the provider is approved for that content. <br>
Risk: The skill installs and relies on the @steipete/summarize npm package. <br>
Mitigation: Install only when the npm package and configured model endpoint are trusted. <br>
Risk: The summarize configuration file may store an API key and default endpoint settings under ~/.summarize/config.json. <br>
Mitigation: Review the configuration file after setup and protect or remove stored credentials when environment variables are preferred. <br>


## Reference(s): <br>
- [Li Summarize on ClawHub](https://clawhub.ai/43622283/li-summarize) <br>
- [summarize CLI](https://summarize.sh) <br>
- [Baidu QianFan](https://cloud.baidu.com/product/wenxinworkshop) <br>
- [Aliyun Dashscope](https://dashscope.aliyuncs.com/) <br>
- [Tencent Hunyuan](https://cloud.tencent.com/product/hunyuan) <br>
- [DeepSeek Platform](https://platform.deepseek.com/) <br>
- [Zhipu AI](https://open.bigmodel.cn/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May generate or update summarize CLI configuration under ~/.summarize.] <br>

## Skill Version(s): <br>
0.0.2 (source: server release metadata; artifact frontmatter says 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
