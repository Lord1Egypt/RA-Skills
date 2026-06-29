## Description: <br>
Perception Music turns local agent perception signals into deterministic WAV or MP3 music using a local FM synthesizer. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[citriac](https://clawhub.ai/user/citriac) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to sonify local perception data such as brightness, RMS, phase, temperature, and presence into audio compositions. It is useful for local, offline perception-to-music workflows that do not require API keys, external calls, or ML models. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads local perception data under ~/.qclaw. <br>
Mitigation: Install and run it only when local perception data access is expected for the workflow. <br>
Risk: The skill executes local binaries such as fm_compose, sense_all, and ffmpeg. <br>
Mitigation: Use trusted local binaries and prefer absolute paths for ffmpeg and related tools. <br>
Risk: Scheduled use can create recurring compositions and local file writes. <br>
Mitigation: Enable scheduled composition only when recurring audio generation is intentional. <br>
Risk: Generated audio is written to ~/.qclaw/workspace/soundscape with temporary WAV or MP3 files created during processing. <br>
Mitigation: Review the output location and storage impact before repeated or automated runs. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/citriac/perception-music) <br>
- [FM Synthesis Algorithm](references/fm_algorithm.md) <br>
- [Perception to Music Mapping](references/perception_mapping.md) <br>


## Skill Output: <br>
**Output Type(s):** [Files, Shell commands, Guidance] <br>
**Output Format:** [WAV or MP3 audio files with terminal status output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reads local perception data, invokes local audio tools, and writes generated audio to the local soundscape workspace.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter, _meta.json, server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
