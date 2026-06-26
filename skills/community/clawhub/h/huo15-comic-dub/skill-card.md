## Description: <br>
Reads a script.json dialogue file, assigns stable voices by character, and uses Volcengine Ark Seed-TTS to generate one WAV file per dialogue line. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhaobod1](https://clawhub.ai/user/zhaobod1) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Comic and audio producers use this skill to turn structured scene dialogue into per-line character voice tracks for downstream editing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a Volcengine Ark API key and sends dialogue text to that provider. <br>
Mitigation: Install only where that provider use is acceptable, and scope ARK_API_KEY to the intended environment. <br>
Risk: TTS generation can incur provider charges based on dialogue length. <br>
Mitigation: Review the script length and expected cost before running, and use the included cost guard for longer jobs. <br>
Risk: Generated audio and manifest files are written to the selected output directory. <br>
Mitigation: Use a dedicated project output directory and review generated files before downstream use. <br>


## Reference(s): <br>
- [Volcengine Text-to-Speech Documentation](https://www.volcengine.com/docs/6561/97465) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Files, JSON] <br>
**Output Format:** [WAV audio files and manifest JSON, produced by a Python command.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires ARK_API_KEY and can incur Volcengine Ark TTS usage charges based on dialogue length.] <br>

## Skill Version(s): <br>
0.1.0 (source: release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
