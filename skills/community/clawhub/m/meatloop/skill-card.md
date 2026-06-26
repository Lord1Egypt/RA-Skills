## Description: <br>
MeatLoop lets agents email a question, screenshot, or pair of images to a human reviewer and receive a structured verdict with optional public verification. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[meatloopservice](https://clawhub.ai/user/meatloopservice) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users can use this skill to request human judgment for binary or near-binary checks, screenshots, generated content, documents, and A/B image comparisons. It is best suited for sanity checks and content verification, not specialist legal, medical, or financial advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Requests and attachments are sent to an external Gmail inbox for human review. <br>
Mitigation: Submit only selected non-sensitive questions or images, and do not send credentials, confidential screenshots, regulated data, or legal, medical, or financial material. <br>
Risk: Human judgments may be subjective, delayed, or outside the service scope. <br>
Mitigation: Use responses as sanity checks, expect best-effort turnaround with no SLA, and treat DEFER or DECLINE outcomes as signals to seek another review path. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/meatloopservice/meatloop) <br>
- [MeatLoop Homepage](https://github.com/meatloopservice/MeatLoop) <br>
- [Public Review Log](https://docs.google.com/spreadsheets/d/e/2PACX-1vTNynmFGYxtUetqMgvGsO4VY6TE_i-ZDdotEFweE_9QsZo4njPpBhrHZ5aYbTC7Ql-8GnwgN2NHnHXi/pub) <br>
- [Verification CSV](https://docs.google.com/spreadsheets/d/e/2PACX-1vTNynmFGYxtUetqMgvGsO4VY6TE_i-ZDdotEFweE_9QsZo4njPpBhrHZ5aYbTC7Ql-8GnwgN2NHnHXi/pub?gid=1119131304&single=true&output=csv) <br>


## Skill Output: <br>
**Output Type(s):** [text, guidance] <br>
**Output Format:** [Plain text email response with structured fields] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Responses may include VERDICT, BETTER IMAGE, REASON, CONFIDENCE, VERIFICATION, and REQUEST-ID fields.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
