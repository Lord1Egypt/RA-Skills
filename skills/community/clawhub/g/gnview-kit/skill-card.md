## Description: <br>
抖音数据分析工具集，包含视频数据分析、用户画像分析、趋势统计等完整分析能力。适用于抖音数据深度挖掘和报告生成场景。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gnview](https://clawhub.ai/user/gnview) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and analysts use this skill to collect Douyin video metadata, download videos, extract scripts or captions, structure analysis results, and synchronize records and linked analysis documents into Feishu Bitable. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can write Douyin analysis records and linked documents into Feishu without clear confirmation or rollback controls. <br>
Mitigation: Use least-privilege Feishu access, limit the target workspace/table, and require explicit preview and confirmation before batch writes or cloud document creation. <br>
Risk: The skill can download videos to a configured local path. <br>
Mitigation: Set a constrained download directory and require explicit confirmation before downloads. <br>
Risk: The skill depends on related skills and API credentials for downloader and analysis workflows. <br>
Mitigation: Review and trust the related skills first, and keep API keys in environment or secret storage rather than committed files. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/gnview/gnview-kit) <br>
- [Publisher profile](https://clawhub.ai/user/gnview) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance] <br>
**Output Format:** [Markdown guidance with structured field definitions and configuration references] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Coordinates Douyin analysis outputs with Feishu Bitable records and linked cloud documents.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
