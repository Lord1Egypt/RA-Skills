## Description: <br>
Generate and edit PowerPoint files with python-pptx, including slide creation, text replacement, and image replacement while preserving layout. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zicheng354-tech](https://clawhub.ai/user/zicheng354-tech) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent builders use this skill to create PowerPoint decks from structured slide content and update existing presentations by replacing text or images while preserving slide layout. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads selected .pptx files and creates new .pptx, image, and demo log files locally. <br>
Mitigation: Run it in a workspace directory and review generated files before sharing or deploying them. <br>
Risk: Path-like presentation titles could affect where generated files are written. <br>
Mitigation: Use simple presentation titles and avoid path separators or filesystem-like names. <br>
Risk: The release evidence includes crypto and purchase capability labels that the security guidance says are unsupported metadata. <br>
Mitigation: Correct those capability labels before relying on them for deployment or policy decisions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zicheng354-tech/ppt-generate-and-edit) <br>


## Skill Output: <br>
**Output Type(s):** [Files, JSON] <br>
**Output Format:** [PowerPoint .pptx files, local image files, file paths, and JSON replacement logs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates new local output files rather than overwriting source presentations.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
