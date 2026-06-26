## Description: <br>
Organize a video folder by cleaning non-video files, removing short or low-quality videos, and classifying videos into numbered subfolders using AI vision analysis. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lemondepat](https://clawhub.ai/user/lemondepat) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
People managing local video folders use this skill to clean a selected folder, identify short or poor-quality clips, and sort remaining videos into language-matched category folders after reviewing the proposed actions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can move or delete files in the selected folder. <br>
Mitigation: Review file lists and proposed actions before execution, keep backups for important videos, and prefer moving files to _misc or _rejected when uncertain. <br>
Risk: Representative frames from videos may expose sensitive content during AI vision analysis. <br>
Mitigation: Use the skill only on folders whose contents are acceptable for frame extraction and analysis, and clean up temporary frames after analysis. <br>
Risk: AI quality checks and category labels may be inaccurate. <br>
Mitigation: Review the summary table and proposed folder structure before allowing files to be moved or deleted. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lemondepat/organise-videos) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with shell command snippets and summary tables] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces folder action plans, category labels, confirmation prompts, and final folder structure summaries.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
