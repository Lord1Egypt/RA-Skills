## Description: <br>
Rebuild, beautify, and optimize editable PowerPoint flowcharts, topology diagrams, architecture diagrams, and process visuals from existing PPT/PPTX files or source images. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xuyongliang-eccom](https://clawhub.ai/user/xuyongliang-eccom) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Presentation authors, consultants, and technical teams use this skill to convert messy or image-based diagram slides into clearer, editable PowerPoint diagrams for review and delivery. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Presentation files may contain sensitive business, architecture, or client information. <br>
Mitigation: Test with non-sensitive decks first and review generated slides before sharing or deploying them. <br>
Risk: The bundled rebuild script processes PPTX files using Python and python-pptx in the user's environment. <br>
Mitigation: Run it only in an environment where Python dependencies are expected and where processing the target presentation is permitted. <br>
Risk: Diagram reconstruction can omit or misread details from low-quality images or cluttered slides. <br>
Mitigation: Compare the rebuilt slide against the source and manually correct labels, connectors, and hierarchy before delivery. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/xuyongliang-eccom/ppt-polish) <br>
- [image-to-ppt-flowchart-sop.md](references/image-to-ppt-flowchart-sop.md) <br>
- [ppt-topology-from-image.md](references/ppt-topology-from-image.md) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance, editable PPTX file outputs, and optional Python-based rebuild commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce optimized .pptx files, rebuilt single-slide diagrams, alternate visual versions, or Markdown/Mermaid structure drafts depending on the request.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
