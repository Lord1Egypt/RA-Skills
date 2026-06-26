## Description: <br>
Local text-to-speech using macOS `say` and ffmpeg for Telegram and Matrix voice messages. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zviratko](https://clawhub.ai/user/zviratko) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to generate local macOS text-to-speech audio, convert it to Opus OGG with ffmpeg, and send it as a voice message in Telegram or Matrix workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The authoritative security summary marks the release suspicious and describes bundled maintenance skills with broad local and service authority. <br>
Mitigation: Review and scan the skill before deployment, install only in environments where this authority is intended, and prefer non-yolo execution modes unless the nested reviewer is explicitly trusted. <br>
Risk: The workflow runs local shell commands and writes temporary audio files. <br>
Mitigation: Confirm generated command targets, keep audio output in an approved workspace directory, and verify `say` and `ffmpeg` availability before use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zviratko/macos-say) <br>
- [Publisher profile](https://clawhub.ai/user/zviratko) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown with inline bash, JSON, and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local audio workflow guidance for AIFF input and Opus OGG output.] <br>

## Skill Version(s): <br>
0.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
