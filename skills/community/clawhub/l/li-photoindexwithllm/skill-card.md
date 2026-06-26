## Description: <br>
PhotoIndexWithLLM indexes local photo collections with vision-language models and lets agents scan, search, annotate, and return structured photo results through a CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[43622283](https://clawhub.ai/user/43622283) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to create a searchable index of photo folders, then answer natural-language photo retrieval requests with text or JSON results. It is suited for personal or workflow-integrated photo search where users can keep photo analysis local by default and explicitly enable remote providers when acceptable. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Photo content may be sent to third-party VL providers when remote models are explicitly enabled. <br>
Mitigation: Keep the default local-only privacy mode for sensitive photos; enable remote models only after user consent and only for content acceptable to send to the configured provider. <br>
Risk: The local SQLite index can expose photo paths, descriptions, tags, and other metadata. <br>
Mitigation: Restrict database file permissions, avoid sharing the index or logs, and delete the local database when the index is no longer needed. <br>
Risk: API keys may be stored in a local .env file for configured model providers. <br>
Mitigation: Keep .env out of version control, limit file permissions to the local user, and rotate provider keys if exposure is suspected. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/43622283/li-photoindexwithllm) <br>
- [English README](artifact/README_EN.md) <br>
- [Agent integration guide](artifact/AGENTS.md) <br>
- [Privacy guide](artifact/PRIVACY_GUIDE.md) <br>
- [Cross-platform verification](artifact/CROSS_PLATFORM_VERIFICATION.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands, Configuration guidance, Code] <br>
**Output Format:** [CLI text or structured JSON, with Markdown documentation and command examples.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Search and statistics outputs can include local photo paths, filenames, tags, descriptions, scene metadata, confidence scores, and processing status.] <br>

## Skill Version(s): <br>
1.1.2 (source: server release evidence and skill.yaml) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
