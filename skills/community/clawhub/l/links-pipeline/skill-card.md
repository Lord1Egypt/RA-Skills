## Description: <br>
Automated link processing pipeline that detects supported video and article links, downloads or extracts content, transcribes or converts it to text, identifies topics, and routes results to a configured knowledge base inbox. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xings117](https://clawhub.ai/user/xings117) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and knowledge workers use this skill to turn incoming Douyin, Xiaohongshu, Bilibili, WeChat, or web article links into stored text artifacts and route them into a configured knowledge base workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can fetch pasted links, save extracted article text or video transcripts locally, upload results through configured COS storage, and send transcript text to DeepSeek when configured. <br>
Mitigation: Use it only for content approved for this workflow, review storage and credential configuration before deployment, and avoid private, regulated, proprietary, or copyrighted content unless explicit confirmation is added. <br>
Risk: The security verdict is suspicious because the workflow can process and route content without a clear confirmation step. <br>
Mitigation: Add an explicit user confirmation or review gate before downloading, uploading, or sending content to external services. <br>


## Reference(s): <br>
- [ClawHub package page](https://clawhub.ai/packages/links-pipeline) <br>
- [ClawHub skill page](https://clawhub.ai/xings117/links-pipeline) <br>
- [DeepSeek API endpoint](https://api.deepseek.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown, JSON status objects, extracted text, transcripts, and shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write local files under /tmp/links-pipeline and may upload processed content through configured object storage.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
