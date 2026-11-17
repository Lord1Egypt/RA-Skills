## Description:

Meeting Transcriber helps an agent start and manage real-time Chinese meeting transcription with FunASR, including environment checks, transcript saving, and meeting-record file access.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chinapjs](https://clawhub.ai/user/chinapjs)

### License/Terms of Use:

MIT-0

## Use Case:

Employees, meeting facilitators, and developers can use this skill to run local Chinese speech-to-text transcription during meetings, save timestamped transcripts, and inspect or open recent meeting records.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill depends on an external local transcription script at D:/dev/python/voiceFunAsr/vocie_mic_fixed_gbk.py that was not included in the reviewed artifact.

Mitigation: Install only after inspecting that script and confirming it matches the intended transcription workflow.

Risk: The skill records microphone audio and creates meeting transcript files, which can expose participant speech and sensitive meeting content.

Mitigation: Obtain participant consent before recording and store generated transcripts according to the organization's data handling policy.

Risk: Environment setup can install or depend on local Conda packages whose versions are not pinned in the artifact.

Mitigation: Pin and review dependencies in the audioProject environment before using the skill in production workflows.

Risk: The stop command terminates processes whose command line contains the transcription-script substring, which may affect unrelated processes.

Mitigation: Review running processes before using the stop command or narrow process matching in the local deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chinapjs/skills/pengjschina-meeting-transcriber)
- [FunASR project](https://github.com/alibaba-damo-academy/FunASR)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Plain text and Markdown-style command guidance with transcript file references]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Starts and stops local microphone transcription, checks the Conda environment, and lists or opens timestamped meeting transcript files.]

## Skill Version(s):

1.0.0 (source: server release evidence and artifact metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
