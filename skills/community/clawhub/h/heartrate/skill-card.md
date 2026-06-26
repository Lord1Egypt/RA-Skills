## Description: <br>
Log heart rate readings, track BPM trends, and set cardiovascular goals. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bytesagain3](https://clawhub.ai/user/bytesagain3) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to record local heart-rate notes, review simple activity history, and export locally stored logs. It should be treated as a personal note logger, not as a medical monitoring or cardiovascular decision tool. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may be mistaken for a medical or heart-rate analytics tool. <br>
Mitigation: Use it only as a local note logger and do not rely on its output for cardiovascular or medical decisions. <br>
Risk: Sensitive health notes may be stored as plaintext local files under ~/.local/share/heartrate/. <br>
Mitigation: Avoid entering sensitive health details unless plaintext local storage is acceptable for the user and environment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/bytesagain3/heartrate) <br>
- [Publisher profile](https://clawhub.ai/user/bytesagain3) <br>
- [BytesAgain homepage](https://bytesagain.com) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Files, Guidance] <br>
**Output Format:** [Plain text and markdown command guidance; the bundled shell script writes local log and export files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Stores entries under ~/.local/share/heartrate/ and can export local data as JSON, CSV, or text.] <br>

## Skill Version(s): <br>
2.0.1 (source: server release metadata; artifact frontmatter reports 2.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
