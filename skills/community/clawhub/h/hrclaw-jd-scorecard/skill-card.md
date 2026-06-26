## Description: <br>
Turn job descriptions and PDF resumes into structured hiring decisions, interview questions, and Feishu/DingTalk-friendly output. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[qinjobs](https://clawhub.ai/user/qinjobs) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Recruiters, hiring managers, and recruiting operations teams use this skill to turn a single-role job description into a repeatable screening scorecard, then score PDF or text resumes against that scorecard. It supports first-pass review, interview-question generation, and Feishu/DingTalk-friendly sharing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Resumes and job descriptions may contain personal or confidential recruiting data. <br>
Mitigation: Use the skill only when authorized to process the provided recruiting materials, and share candidate details in Feishu, DingTalk, or other tools only when that sharing is approved. <br>
Risk: Scorecards and resume scores can be incomplete or misleading if the JD is vague, the resume text is missing, or the PDF is image-only. <br>
Mitigation: Review outputs before making hiring decisions, calibrate thresholds with real screening results, and return needs_ocr rather than guessing when PDF text cannot be extracted. <br>
Risk: Automated screening can overstate fit when evidence is inferred beyond the supplied JD, resume, or scorecard. <br>
Mitigation: Keep scoring tied to explicit evidence, use null or empty values for missing information, and treat the result as first-pass support for a human recruiter or hiring manager. <br>


## Reference(s): <br>
- [Quickstart](artifact/references/quickstart.md) <br>
- [FAQ](artifact/references/faq.md) <br>
- [Limitations](artifact/references/limitations.md) <br>
- [ClawHub skill page](https://clawhub.ai/qinjobs/hrclaw-jd-scorecard) <br>
- [Publisher profile](https://clawhub.ai/user/qinjobs) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance] <br>
**Output Format:** [JSON objects for scorecards and resume scores, with optional Markdown or chat-ready Markdown views] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs are evidence-grounded screening artifacts; image-only PDFs should return needs_ocr instead of guessed content.] <br>

## Skill Version(s): <br>
0.1.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
