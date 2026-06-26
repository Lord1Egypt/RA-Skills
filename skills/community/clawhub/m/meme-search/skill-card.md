## Description: <br>
用表情包图片丰富 Agent 表达。可以使用图片使用表情包表达情绪、状态、反应、场景。支持在 SOUL.md 中免安装配置。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[laizhenjie0107](https://clawhub.ai/user/laizhenjie0107) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents use this skill to search for meme images that express the agent's current emotion, status, reaction, or situation, then embed the image directly in a Markdown reply. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Meme search text is sent to an external plain-HTTP service, and replies may embed remote images returned by that service. <br>
Mitigation: Avoid using this skill in conversations containing secrets, private customer data, or sensitive work context; prefer HTTPS or a trusted proxy for sensitive environments. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/laizhenjie0107/meme-search) <br>
- [Meme search API endpoint](http://101.200.84.220/api/v1/meme/search?query={query}) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with image embeds and optional curl examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May return an empty string when the external service fails or rate limits.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
