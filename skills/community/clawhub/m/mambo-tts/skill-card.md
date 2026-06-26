## Description: <br>
Quick-access TTS preset for a lively and energetic Chinese female voice, based on Microsoft Edge TTS. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[systiger](https://clawhub.ai/user/systiger) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and users generating Chinese speech use this skill to invoke preset Edge TTS voices for lively, fast-paced, general, or narration-style audio without remembering detailed voice parameters. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Text submitted for conversion may be sent to Microsoft Edge TTS. <br>
Mitigation: Avoid submitting secrets, private personal data, regulated content, or confidential business material unless that provider use is acceptable. <br>
Risk: The skill depends on Node.js, node-edge-tts, and the neighboring edge-tts converter script. <br>
Mitigation: Confirm those dependencies are installed and trusted before invoking the preset scripts. <br>


## Reference(s): <br>
- [Mambo TTS on ClawHub](https://clawhub.ai/systiger/mambo-tts) <br>
- [Edge TTS Skill](../edge-tts/SKILL.md) <br>
- [node-edge-tts guide](../edge-tts/references/node_edge_tts_guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Files, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands; runtime scripts produce MP3 audio files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [MP3 files are saved to the default workspace output directory; submitted text is sent to Microsoft Edge TTS.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
