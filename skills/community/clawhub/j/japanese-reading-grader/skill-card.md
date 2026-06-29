## Description: <br>
日语朗读作业AI批改（教师模式）——支持音频转写、CEFR分级评价、纠错与成绩录入。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bianmaxingkong](https://clawhub.ai/user/bianmaxingkong) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Teachers use this skill to grade Japanese reading-aloud audio submissions, transcribe audio with local Whisper, provide CEFR-aligned feedback, record Canvas grades, and generate class summaries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow can post Canvas grades and upload class summaries without an explicit confirmation step. <br>
Mitigation: Manually review every grade, comment, course ID, assignment ID, student ID, and summary file before running Canvas posting or upload commands. <br>
Risk: Audio transcription uncertainty can lead to incorrect grading feedback. <br>
Mitigation: Use the artifact's alignment check against the standard answer and send uncertain, missing, extra, or failed transcriptions to manual review instead of automatic scoring. <br>
Risk: Canvas credentials and permissions are not described by the artifact. <br>
Mitigation: Confirm credential storage, scope, and access controls before use, and run the workflow only for Canvas courses the user controls. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/bianmaxingkong/skills/japanese-reading-grader) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown-style guidance with plain-text grading feedback and bash command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Feedback comments are capped at 1000 characters; batch processing guidance limits a run to 50 students.] <br>

## Skill Version(s): <br>
2.2.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
