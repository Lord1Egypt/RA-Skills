## Description: <br>
PNG图片LSB隐写分析、块信息解析与CRC校验工具，支持提取sRGB/gAMA/pHYs元数据并检测多种LSB隐藏模式；适合CTF比赛场景，当用户需要分析PNG图片结构、验证数据完整性、检测隐写信息或提取图像元数据时使用 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Moxin1044](https://clawhub.ai/user/Moxin1044) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, security analysts, and CTF participants use this skill to inspect PNG structure, validate chunk CRCs, extract common PNG metadata, and check selected LSB steganography patterns in user-provided PNG files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Untrusted or very large PNG inputs can still carry normal image-parser risk. <br>
Mitigation: Analyze only files you intentionally choose and apply normal caution for untrusted or unusually large images. <br>
Risk: The optional output path writes a JSON result file and could overwrite an unintended path. <br>
Mitigation: Choose the --output path deliberately and review it before running the command. <br>
Risk: LSB decoding can surface coincidental printable text that is not real hidden content. <br>
Mitigation: Treat LSB results as investigative signals and confirm findings with CRC, metadata, and manual review. <br>


## Reference(s): <br>
- [LSB Pattern Reference](references/lsb_patterns.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/Moxin1044/png-lsb-skills) <br>
- [ClawHub Publisher Profile](https://clawhub.ai/user/Moxin1044) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, JSON, Guidance] <br>
**Output Format:** [Markdown guidance with bash command examples and optional JSON analysis output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The optional --output path writes analysis results as JSON; otherwise results are printed for review.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
