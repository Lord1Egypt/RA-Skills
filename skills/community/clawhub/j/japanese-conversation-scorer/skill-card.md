## Description: <br>
日语会话作业AI批改，支持语音转写、CEFR分级评价、纠错与Canvas成绩录入。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bianmaxingkong](https://clawhub.ai/user/bianmaxingkong) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Teachers use this skill to grade Japanese conversation audio assignments, produce concise student feedback, and record grades in Canvas. It supports classroom workflows that require transcription, CEFR-aligned assessment, correction guidance, and class summaries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow handles sensitive student records, local audio files, transcripts, and submission maps. <br>
Mitigation: Restrict access to authorized staff, avoid shared temporary storage, and delete local audio, transcripts, and maps after grading. <br>
Risk: The workflow can upload Canvas grades and feedback. <br>
Mitigation: Require human review before uploads and confirm the Canvas assignment is configured for controlled grade release. <br>
Risk: Use may be subject to school privacy, records, and grading policies. <br>
Mitigation: Confirm institutional approval and policy compliance before installation or classroom use. <br>


## Reference(s): <br>
- [日语会话作业批改 - 详细流程](artifact/references/workflow.md) <br>
- [ClawHub skill page](https://clawhub.ai/bianmaxingkong/skills/japanese-conversation-scorer) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown feedback templates with inline shell commands and Canvas workflow guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce student feedback, grade values, transcript references, and class summary guidance.] <br>

## Skill Version(s): <br>
1.1.6 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
