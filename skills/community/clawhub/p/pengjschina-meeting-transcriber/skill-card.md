## Description: <br>
Meeting Transcriber provides Chinese real-time meeting speech transcription with FunASR, timestamped transcript files, environment checks, and Conda setup guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chinapjs](https://clawhub.ai/user/chinapjs) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Meeting participants, facilitators, and OpenClaw users use this skill on a Windows workstation to start and stop Chinese speech transcription, check the local audio and Conda environment, and manage saved meeting transcript files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security review says the actual recording and transcription runs through an external local script that is not included in the package. <br>
Mitigation: Install only after reviewing and trusting the local D:/dev/python/voiceFunAsr/vocie_mic_fixed_gbk.py script and confirming it matches the intended transcription workflow. <br>
Risk: The artifact uses hard-coded Windows, Conda, and project-directory paths. <br>
Mitigation: Run the environment check before use and verify the audioProject Conda environment, microphone access, and configured meeting_records directory on the target workstation. <br>
Risk: The skill records meeting audio and saves transcripts locally. <br>
Mitigation: Obtain participant consent before recording, confirm where transcript files are saved, and stop the spawned transcription process or window when the meeting ends. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/chinapjs/pengjschina-meeting-transcriber) <br>
- [FunASR project](https://github.com/alibaba-damo-academy/FunASR) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Plain text command responses with transcript file paths; generated meeting records are text files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The skill starts local transcription processes and manages meeting record files under the configured Windows project directory.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and artifact metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
