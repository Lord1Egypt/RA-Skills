## Description:

知识获取：多平台内容解析（小红书/微信/网站等）、8类分类、Markdown 笔记生成、可选飞书云盘归档

This skill is ready for commercial/non-commercial use.

## Publisher:

[yz6214589-hash](https://clawhub.ai/user/yz6214589-hash)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and knowledge workers use this skill to turn links or text from supported platforms into categorized Markdown notes, with optional archival to Feishu cloud storage.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Configured Feishu uploads may become externally accessible links.

Mitigation: Use a dedicated low-privilege Feishu app and folder, review sharing permissions, and disable Feishu archival when testing.

Risk: The skill fetches arbitrary user-provided URLs during link-to-note ingestion.

Mitigation: Avoid submitting confidential or internal URLs and deploy with strict outbound network controls.

Risk: Browser-based extraction can expand runtime exposure if Chromium is run without isolation.

Mitigation: Keep Chromium sandboxing enabled and run the skill in a constrained execution environment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yz6214589-hash/skills/knowledge-acquisition)
- [README](README.md)
- [Workflow guide](WORKFLOW_GUIDE.md)
- [Dependencies](DEPENDENCIES.md)
- [Classification accuracy report](reports/classification-accuracy-report.md)
- [Exception scenarios report](reports/exception-scenarios-report.md)
- [Performance benchmark report](reports/performance-benchmark-report.md)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown notes with classification metadata, source details, media lists, trace IDs, and optional Feishu document links.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include category confidence, keyword evidence, retry status, and archival URLs when configured.]

## Skill Version(s):

2.0.1 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
