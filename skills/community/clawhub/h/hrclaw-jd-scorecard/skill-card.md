## Description:

Turn job descriptions and PDF resumes into structured hiring decisions, interview questions, and Feishu/DingTalk-friendly output.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qinjobs](https://clawhub.ai/user/qinjobs)

### License/Terms of Use:

MIT-0

## Use Case:

Recruiters, hiring managers, and recruiting operations teams use this skill to convert a single-role JD into a repeatable screening scorecard, generate interview questions, and score PDF or pasted-text resumes against that scorecard.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Resume scoring can expose personal data from resumes and packaged examples.

Mitigation: Use only resumes the user is authorized to process, redact names, employers, and resume excerpts before sharing results, and replace candidate-like examples with fully synthetic data.

Risk: Implicit handling of attached PDFs can process sensitive resume content before the user has supplied a scorecard or confirmed intent.

Mitigation: Ask for a JD or scorecard before scoring a resume, avoid implicit processing of attachments, and stop with needs_scorecard or needs_ocr when required inputs are missing.

Risk: Automated scorecards and scores may be treated as final hiring decisions or may overstate evidence from vague JDs and resumes.

Mitigation: Use outputs as a first-pass screening aid, rely only on explicit JD and resume evidence, add assumptions instead of guessing, and have recruiters or hiring managers review thresholds and decisions.

## Reference(s):

- [Quickstart](references/quickstart.md)
- [FAQ](references/faq.md)
- [Limitations](references/limitations.md)
- [JD to scorecard prompt](prompts/jd-to-scorecard.md)
- [Resume scoring prompt](prompts/resume-score.md)
- [Interview questions prompt](prompts/interview-questions.md)
- [Scorecard JSON template](templates/scorecard.json)
- [Resume score JSON template](templates/resume-score.json)

## Skill Output:

**Output Type(s):** [JSON, Markdown, Guidance]

**Output Format:** [JSON objects with optional Markdown scorecard, resume-score, and team-chat views]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns scorecard JSON first for JD analysis and resume scoring JSON first for resumes; uses needs_ocr when an image-only PDF has no extractable text.]

## Skill Version(s):

0.1.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
