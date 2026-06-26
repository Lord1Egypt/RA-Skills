## Description: <br>
Provides Windows-oriented music search, authorized MP3 download, ID3 metadata embedding, and local playback commands using multiple music API sources. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[freebook8](https://clawhub.ai/user/freebook8) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Windows users and agents use this skill to search supported music APIs, download tracks they are authorized to download, add ID3 metadata, and open local audio files in the system player. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can download music from public API sources, which may include content the user is not authorized to download. <br>
Mitigation: Use it only for music you are authorized to download and comply with the applicable music service and content terms. <br>
Risk: Some scripts include hard-coded Windows demo paths and default download locations. <br>
Mitigation: Review command arguments and default paths before running, and provide an explicit output path when possible. <br>
Risk: Dependencies are broad and not pinned in the artifact metadata. <br>
Mitigation: Pin or minimize dependencies before installing in a sensitive environment. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/freebook8/music-player) <br>
- [go-music-api project](https://github.com/caorushizi/go-music-api) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Code, Configuration] <br>
**Output Format:** [Markdown with inline shell commands and file path guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands may create MP3 files, update ID3 metadata, or launch local playback when run.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata, package.json, artifact changelog) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
