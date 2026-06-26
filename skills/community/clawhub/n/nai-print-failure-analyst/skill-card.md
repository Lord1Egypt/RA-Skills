## Description: <br>
Diagnose 3D print failures by symptoms or images, recommend slicer setting fixes, log issues, view history, and generate failure reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[newageinvestments25-byte](https://clawhub.ai/user/newageinvestments25-byte) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, makers, and 3D printer operators use this skill to diagnose failed prints, compare likely causes, apply slicer-setting fixes, and maintain a local history of recurring failures. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The local failure history can contain user-provided printer details, materials, descriptions, slicer settings, fixes, and notes. <br>
Mitigation: Avoid putting unrelated private details in failure descriptions or notes. <br>
Risk: Markdown reports can be saved to a user-specified output path. <br>
Mitigation: Review the report output path before saving a report. <br>


## Reference(s): <br>
- [3D Print Failure Types](references/failure-types.md) <br>
- [Slicer Setting Fixes by Failure Type](references/slicer-fixes.md) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Guidance, Shell commands, Markdown, JSON, Files] <br>
**Output Format:** [Markdown guidance with optional JSON and markdown reports from helper scripts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write a local JSON failure log and markdown report when the user asks.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
