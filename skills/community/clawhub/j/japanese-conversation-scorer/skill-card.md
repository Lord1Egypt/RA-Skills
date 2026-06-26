## Description: <br>
Japanese language teachers use this skill to batch review student speaking-assignment audio by transcribing responses, scoring them with a CAF rubric, generating corrections, and preparing class summaries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bianmaxingkong](https://clawhub.ai/user/bianmaxingkong) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Japanese language teachers use this skill to grade oral-conversation assignments submitted as audio, provide concise encouraging feedback, and prepare scores or class-level summaries for posting. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Student audio, transcripts, and grades are sensitive education records. <br>
Mitigation: Use the skill only when authorized to handle submissions and grades, keep local copies in a controlled location, and delete them when no longer needed. <br>
Risk: Automated transcription or scoring errors could affect student grades. <br>
Mitigation: Treat Whisper transcripts as reference material, perform alignment checks, and manually verify scores before posting grades. <br>
Risk: Download or upload scripts may move student data outside the expected location. <br>
Mitigation: Review any external scripts before running them and confirm upload targets before posting summaries or grades. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/bianmaxingkong/japanese-conversation-scorer) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown-style grading feedback with inline shell commands and spreadsheet-oriented class summary guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses local Whisper medium transcription; grades and transcripts should be manually verified before posting.] <br>

## Skill Version(s): <br>
1.1.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
