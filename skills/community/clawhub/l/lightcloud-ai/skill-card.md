## Description: <br>
Integrate with Qingyun/Lightcloud API to manage form documents by helping agents fetch access tokens and retrieve, create, update, or delete form data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wzy2008a](https://clawhub.ai/user/wzy2008a) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to prepare Lightcloud API calls from natural-language requests, including authentication and form document retrieval, creation, update, and deletion workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill helps construct API calls that use Lightcloud credentials and access tokens. <br>
Mitigation: Use least-privilege credentials and avoid pasting production secrets into shared chats, logs, or transcripts. <br>
Risk: Some generated commands can create, update, or delete Lightcloud form records. <br>
Mitigation: Manually verify workspace, form, and record IDs before running any record-changing command. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wzy2008a/lightcloud-ai) <br>
- [轻云开放API参考文档](references/api_reference.md) <br>
- [OpenClaw](https://github.com/openclaw/openclaw) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with curl, PowerShell, and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include credential placeholders, timestamps, API endpoints, request bodies, and verification guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
