## Description: <br>
PM Interview Coach helps candidates practice product manager interviews by using a resume, target company and role, optional job description, recent Xiaohongshu interview reports, and structured answer guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[krisdontknowcoding](https://clawhub.ai/user/krisdontknowcoding) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users preparing for product manager interviews use this skill to run single-round mock interviews, receive resume deep-dive questions, practice business scenario questions, and review detailed answer frameworks and feedback. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses Xiaohongshu MCP access and MiniMax-VL-01 for interview-content research, which may expose resume, target-role, or interview-prep context depending on the user's setup. <br>
Mitigation: Redact unnecessary personal details, verify whether the MCP and model setup is local or hosted, and share only information needed for the simulation. <br>
Risk: The helper can save interview-post images under ~/.openclaw/workspace/xhs_interview_images. <br>
Mitigation: Periodically remove saved images and avoid retaining screenshots that contain personal, confidential, or proprietary information. <br>


## Reference(s): <br>
- [PM Interview Coach README](README.md) <br>
- [Behavioral Questions Reference](references/behavioral-questions.md) <br>
- [Business Framework Reference](references/business-framework.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/krisdontknowcoding/pm-interview-coach) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown interview questions, coaching feedback, evaluation tables, and reference answers] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs are tailored to the user's resume, target company, role, optional job description, and confirmed interview round.] <br>

## Skill Version(s): <br>
1.4.4 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
