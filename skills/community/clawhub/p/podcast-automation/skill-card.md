## Description: <br>
播客全流程自动化: 抓取、转录、Sonos播放、飞书Wiki归档。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[terrycarter1985](https://clawhub.ai/user/terrycarter1985) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and podcast operators use this skill to download podcast audio, transcribe it locally, play selected episodes on Sonos speakers, and archive transcript notes to Feishu Wiki. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Transcript content may be uploaded to the wrong Feishu Wiki space or include sensitive podcast notes. <br>
Mitigation: Review transcript contents and the destination space before archiving. <br>
Risk: Feishu app credentials can grant more access than the archive workflow needs. <br>
Mitigation: Use least-privilege Feishu app credentials and rotate them according to the user's credential policy. <br>
Risk: Unpinned external tools can change behavior across installs. <br>
Mitigation: Pin external tool versions when reproducible installs are required. <br>
Risk: Sonos playback commands can affect the wrong speaker on the local network. <br>
Mitigation: Confirm the target speaker name before issuing playback or volume commands. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/terrycarter1985/podcast-automation) <br>
- [archive-to-wiki.sh](references/scripts/archive-to-wiki.sh) <br>
- [sonoscli Go module](https://github.com/steipete/sonoscli) <br>
- [openai-whisper package](https://pypi.org/project/openai-whisper/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with bash commands and environment-variable configuration] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses local audio files, named Sonos speakers, and Feishu app credentials when archiving transcripts.] <br>

## Skill Version(s): <br>
3.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
