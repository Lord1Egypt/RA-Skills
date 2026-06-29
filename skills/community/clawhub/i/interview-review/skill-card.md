## Description: <br>
This skill helps job seekers review real interview transcripts or written Q&A, identify strengths and risks, infer interviewer intent, and produce concrete improvement advice. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shutongzhou1222](https://clawhub.ai/user/shutongzhou1222) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External job seekers use this skill after an interview to turn supplied transcript text or remembered Q&A into a structured Chinese-language review report. The skill evaluates overall performance, highlights up to a few strengths and risks, reviews the most consequential questions, and recommends specific next actions without inventing missing facts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Interview transcripts and notes can contain sensitive career, employer, compensation, or personal information. <br>
Mitigation: Share only details you are comfortable providing to the agent, and omit or generalize sensitive names, compensation details, or personal identifiers when they are not needed for the review. <br>
Risk: The skill cannot directly listen to audio recordings or read external systems. <br>
Mitigation: Provide a text transcript or written Q&A in the conversation before expecting a review. <br>
Risk: Review quality depends on the completeness of the supplied interview content and role context. <br>
Mitigation: Provide the interview Q&A plus role, industry, and round when available; when key context is missing, the skill should ask for it or clearly mark conclusions as uncertain. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/shutongzhou1222/skills/interview-review) <br>
- [Publisher profile](https://clawhub.ai/user/shutongzhou1222) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Structured Chinese-language Markdown report] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The report is limited to user-provided interview content, emphasizes uncertainty when details are missing, and avoids JSON output.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
