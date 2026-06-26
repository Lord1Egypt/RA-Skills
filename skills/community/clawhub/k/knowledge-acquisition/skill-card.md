## Description: <br>
知识获取 parses links or text from supported content platforms, classifies the material, generates Markdown notes, and can optionally archive them to Feishu Drive. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yz6214589-hash](https://clawhub.ai/user/yz6214589-hash) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to turn links or text from supported platforms into categorized Markdown knowledge notes, with optional Feishu Drive archival and notification. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: When Feishu credentials are configured, extracted content, generated notes, metadata, and file tokens may be uploaded to Feishu and made accessible to anyone with the link. <br>
Mitigation: Use least-privilege Feishu credentials, review sharing permissions before upload, and set FEISHU_DISABLED=true for local-only use. <br>
Risk: The skill depends on sensitive credentials for Feishu archival and may also use a GitHub token for higher API limits. <br>
Mitigation: Provide secrets through managed environment variables or a secrets manager, and keep credentials out of files, prompts, and logs. <br>
Risk: Private, regulated, or proprietary content could be included in extracted notes and then shared through Feishu. <br>
Mitigation: Review source content and generated notes before archival, and use private sharing settings for sensitive material. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/yz6214589-hash/knowledge-acquisition) <br>
- [README](artifact/README.md) <br>
- [Workflow guide](artifact/WORKFLOW_GUIDE.md) <br>
- [Dependencies](artifact/DEPENDENCIES.md) <br>
- [Feishu Open Platform](https://open.feishu.cn) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Files, Configuration guidance] <br>
**Output Format:** [Markdown notes and plain-text status messages with optional Feishu document URL and token.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js and optional Feishu credentials; Feishu archival can be skipped with FEISHU_DISABLED=true.] <br>

## Skill Version(s): <br>
2.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
