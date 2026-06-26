## Description: <br>
Converts OpenMAIC course JSON files into PPTX presentations with optional speaker notes using a local Node.js exporter. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[taizhouchen](https://clawhub.ai/user/taizhouchen) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to export existing OpenMAIC course content as shareable PowerPoint files, optionally preserving speaker notes for presentation delivery. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Cleanup instructions can remove unrelated PPTX files from the user's workspace. <br>
Mitigation: Delete only the exact generated PPTX file after confirming it is no longer needed; avoid wildcard cleanup commands. <br>
Risk: Generated presentations can include speaker notes that may contain sensitive course content. <br>
Mitigation: Review the PPTX before sharing, or run the exporter with --no-notes when notes should be excluded. <br>
Risk: The exporter runs local Node.js code against a local OpenMAIC installation. <br>
Mitigation: Use it only with a trusted OpenMAIC directory and expected course files. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/taizhouchen/openmaic-convert-pptx) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Files, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands; runtime script generates PPTX files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated PPTX files may include speaker notes unless the --no-notes option is used.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
