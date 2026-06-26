## Description: <br>
使用 NotebookLM CLI 生成 PPT 演示文稿，从预置风格模板库中选择模板，通过 notebook query 设置风格要求，再生成幻灯片。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yenava](https://clawhub.ai/user/yenava) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to turn NotebookLM source material into a PPTX slide deck with a selected presentation style template. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow sends source documents and generated slide content through NotebookLM and an external CLI. <br>
Mitigation: Use only an approved NotebookLM account, verify the notebooklm-mcp-cli package source, and avoid confidential documents unless NotebookLM is approved for that data. <br>
Risk: The workflow downloads and sends a PPTX file that may not be the intended artifact. <br>
Mitigation: Record the returned Artifact ID and send only the specific PPTX file intended for sharing. <br>


## Reference(s): <br>
- [NotebookLM PPT style templates](artifact/references/templates.md) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Guidance, Files] <br>
**Output Format:** [Markdown guidance with inline shell commands and a generated PPTX file workflow] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses a NotebookLM account through the notebooklm-mcp-cli package and sends the downloaded PPTX from the OpenClaw inbound media directory.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
