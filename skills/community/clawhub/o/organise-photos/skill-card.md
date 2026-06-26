## Description: <br>
Organize a photo folder by cleaning non-photo files, removing bad exposures, detecting blur and burst shots, and classifying photos into numbered subfolders using AI vision analysis. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lemondepat](https://clawhub.ai/user/lemondepat) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill to organize a selected photo folder by separating non-photo files, reviewing poor exposures, detecting blur and burst groups, and sorting photos into numbered content categories. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can move or delete photos and other files in the selected folder. <br>
Mitigation: Use a backed-up copy first, review all proposed changes, and prefer move-to-review options instead of deletion when possible. <br>
Risk: The skill may install Python image-processing packages if dependencies are missing. <br>
Mitigation: Preinstall the listed packages in a virtual environment before running the skill. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lemondepat/organise-photos) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with shell and Python code blocks, summaries, and confirmation prompts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May move or delete files in the selected folder after user confirmation; supports language-matched folder names.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
