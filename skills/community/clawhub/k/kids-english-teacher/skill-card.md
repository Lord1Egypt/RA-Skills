## Description: <br>
Generates a bilingual, interactive HTML English lesson from a child's English homework photo, including vocabulary practice, pronunciation, writing correction, phonics, dialogue exercises, rewards, and browser microphone-based reading practice. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ifeychan702](https://clawhub.ai/user/ifeychan702) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and caregivers use this skill to turn a child's photographed English homework into a downloadable, local HTML learning page. It is intended for image-based children's homework practice, not general adult English tutoring or text-only exercises. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The generated lesson may contain content extracted from a child's homework image. <br>
Mitigation: Review the generated HTML before sharing it and remove any sensitive child or homework details that should not be retained. <br>
Risk: Reading practice can request browser microphone access for speech recognition. <br>
Mitigation: Use microphone features only with guardian approval, or edit the generated page to remove the microphone workflow. <br>
Risk: The generated HTML can reference Google Fonts, creating an external network request when opened. <br>
Mitigation: Remove or replace the font link before use when offline or more private operation is required. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ifeychan702/kids-english-teacher) <br>
- [Google Fonts dependency](https://fonts.googleapis.com/css2?family=Fredoka+One&family=Nunito:wght@400;700;900&display=swap) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Code, Files, Markdown, Guidance] <br>
**Output Format:** [Downloadable single-file HTML lesson with concise explanatory text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated page may use browser speech synthesis, browser speech recognition, a Google Fonts stylesheet, and locally saved child homework content.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
