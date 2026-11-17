## Description:

Daily IELTS practice coach for Band 5.5 learners aiming for Band 6.0-6.5, with rotating Listening, Reading, Writing, and Speaking homework plus structured feedback.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cngvc](https://clawhub.ai/user/cngvc)

### License/Terms of Use:

MIT-0

## Use Case:

External IELTS learners and their agents use this skill to generate one focused daily practice session, rotate across exam skills, and receive Band 6-oriented feedback after responses.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill writes a small local progress file to rotate IELTS topics.

Mitigation: Install and run it with normal skill-scoped file permissions and review any filesystem writes during deployment.

Risk: Generated IELTS scoring and feedback may be imperfect or overly strict because it is agent-produced guidance.

Mitigation: Use the feedback for practice support and review important scoring decisions against official IELTS criteria or a qualified instructor.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cngvc/skills/ielts-practice)
- [Publisher profile](https://clawhub.ai/user/cngvc)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown-formatted coaching prompts and feedback]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generates original IELTS-style practice content in English, delays answers until the learner responds, and uses a local progress file for topic rotation.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
