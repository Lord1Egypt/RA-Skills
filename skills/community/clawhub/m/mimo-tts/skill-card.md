## Description: <br>
Uses the Xiaomi MiMo TTS API to synthesize styled speech and produce WAV audio from user-provided text. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[whmmy](https://clawhub.ai/user/whmmy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to turn requested text or voice replies into styled speech through Xiaomi MiMo TTS, including voice and style selection with WAV file output. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Text submitted for synthesis is sent to Xiaomi MiMo's API. <br>
Mitigation: Avoid sending secrets or highly sensitive private content for speech synthesis. <br>
Risk: The skill requires a MiMo API key for API access. <br>
Mitigation: Use an API key intended for this purpose and manage it through the MIMO_API_KEY environment variable or approved OpenClaw configuration. <br>
Risk: The helper script can write WAV files to a chosen output path. <br>
Mitigation: Choose output paths intentionally and review generated files before sharing or deploying them. <br>


## Reference(s): <br>
- [Xiaomi MiMo API endpoint](https://api.xiaomimimo.com/v1) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Files, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands; WAV audio file or binary audio bytes when the helper script is run.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses MIMO_API_KEY and can write WAV output to a user-selected path.] <br>

## Skill Version(s): <br>
1.0.2 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
