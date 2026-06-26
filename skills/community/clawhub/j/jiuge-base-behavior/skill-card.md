## Description: <br>
A local audio-processing skill that packages a Jiuge Flow shell workflow for vocal separation, dereverberation, and MP3 mastering. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lzgsrbs](https://clawhub.ai/user/lzgsrbs) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Audio producers and local automation users can use this skill to run a three-step 48 kHz audio workflow that separates vocals, applies dereverberation, and exports master and preview MP3 files. Users should first review the listing mismatch noted by the security scan. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The registry metadata describes a broad behavior-control skill, while the packaged files implement a local audio-processing workflow. <br>
Mitigation: Review the packaged files and install only if the intended use is running the local audio workflow. <br>
Risk: The script depends on hardcoded local tool and model paths and writes processed audio under ~/Desktop/Jiuge_Audio_Projects. <br>
Mitigation: Verify dependency paths, model availability, input locations, and output retention expectations before execution. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/lzgsrbs/jiuge-base-behavior) <br>
- [Packaged skill documentation](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown documentation with bash command examples and a packaged shell script] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The workflow produces local WAV intermediates plus 320 kbps master and 128 kbps preview MP3 files when executed.] <br>

## Skill Version(s): <br>
1.0.1 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
