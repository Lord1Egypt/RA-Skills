## Description: <br>
基于官方违禁词库，覆盖公众号、小红书、抖音三大平台审核标准，支持文案、文件、图片、链接多形式输入，快速输出违禁词标记与上下文替换建议。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[if530770](https://clawhub.ai/user/if530770) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External creators, brand marketers, MCN agencies, and content review teams use this skill to check copy, text files, image text, and webpage text for platform-specific prohibited words before publishing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Checked copy, extracted file text, fetched webpage text, and the REDFOX_API_KEY may be sent to RedFox or a configured HTTPS gateway. <br>
Mitigation: Use an ephemeral or revocable API key, avoid submitting secrets or regulated documents, and route requests through an approved HTTPS gateway when required. <br>
Risk: Persistent shell-profile credential storage can expose the API key to future sessions or other tools on the same account. <br>
Mitigation: Prefer a managed secret store or session-scoped environment variable, and rotate the key if it is exposed in prompts, logs, or files. <br>
Risk: URL checking performs outbound network access and may retrieve private or sensitive pages if such links are provided. <br>
Mitigation: Submit only public or approved URLs, and review link targets before allowing the skill to fetch webpage text. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/if530770/prohibited-word-query) <br>
- [RedFox service](https://redfox.hk) <br>
- [RedFox API key settings](https://redfox.hk/settings/api-keys?source=clawhub) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown text with prohibited-word highlights, replacement tables, optimized copy, and occasional shell commands for API-key configuration.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May call a remote prohibited-word service and may extract text from files, images, or provided URLs before producing the final report.] <br>

## Skill Version(s): <br>
1.0.9 (source: ClawHub server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
