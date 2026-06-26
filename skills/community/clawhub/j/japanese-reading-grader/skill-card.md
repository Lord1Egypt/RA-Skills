## Description: <br>
为日语教师和学习者提供朗读作业批改流程，覆盖音频转写、宽松评分、发音纠错、薄弱点分析和练习建议生成。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bianmaxingkong](https://clawhub.ai/user/bianmaxingkong) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Teachers use this skill to batch grade Japanese reading audio for A1/A2/B1 learners, generate per-student feedback, and prepare class scoring records. Students may also use the workflow for adaptive self-checks when the same answer text and privacy controls are in place. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Student audio, transcripts, reports, and progress files may contain personal or educational records stored locally. <br>
Mitigation: Use a dedicated working directory, restrict access to generated files, and apply the school or organization's privacy and retention rules before using real submissions. <br>
Risk: Local report files or moved failed audio files may overwrite or displace original student work if paths are reused. <br>
Mitigation: Back up originals, use unique report filenames, and review the error-audio folder before cleanup or resubmission. <br>
Risk: Speech transcription uncertainty can lead to incorrect grading decisions. <br>
Mitigation: Treat failed or uncertain transcription as a manual review case before finalizing grades. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/bianmaxingkong/japanese-reading-grader) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with plain-text grading report templates and local file-path conventions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces student-facing feedback, score summaries, review flags for failed or uncertain transcription, and local report/progress file paths.] <br>

## Skill Version(s): <br>
2.1.6 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
