## Description: <br>
Daily IELTS practice coach targeting Band 6.0-6.5, delivering one focused session per skill across Listening, Reading, Writing, and Speaking with structured feedback. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cngvc](https://clawhub.ai/user/cngvc) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External IELTS learners use this skill to receive daily Band 6.0-6.5 practice across Listening, Reading, Writing, and Speaking. The agent generates exam-style homework, waits for the learner's answers, then provides targeted scoring and improvement guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may persist a small local rotation state between sessions. <br>
Mitigation: Delete or reset memory/ielts-state.md if the learner wants to restart the practice rotation. <br>
Risk: Generated IELTS scoring and coaching feedback may be imperfect. <br>
Mitigation: Review important feedback against official IELTS criteria or with a qualified instructor before relying on it for exam preparation. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/cngvc/ielts-practice) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Markdown practice prompts and feedback in English] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May update memory/ielts-state.md to remember the next lesson type in the rotation.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
