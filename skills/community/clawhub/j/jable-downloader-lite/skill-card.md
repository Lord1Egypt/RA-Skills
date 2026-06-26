## Description: <br>
Simple video downloader for Jable.tv. Download videos by ID or search by actress name. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hs9021401](https://clawhub.ai/user/hs9021401) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to have an agent download Jable.tv videos by video ID or actress search and organize the resulting files in a local Videos directory. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill runs yt-dlp and ffmpeg and accesses Jable.tv over the network. <br>
Mitigation: Install and run it only in environments where those external tools and that site access are acceptable. <br>
Risk: The skill saves downloaded adult videos under the default Videos folder or a user-selected directory. <br>
Mitigation: Review the requested download count and destination before execution, especially on shared machines. <br>
Risk: The skill may download multiple videos when searching by actress name. <br>
Mitigation: Set a specific count and verify available disk space before starting a search download. <br>


## Reference(s): <br>
- [ClawHub package page](https://clawhub.ai/hs9021401/jable-downloader-lite) <br>
- [Jable.tv](https://jable.tv/) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Files, Guidance] <br>
**Output Format:** [Console progress text and downloaded video files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Downloads are saved under the system Videos folder or a chosen directory and organized by actress name.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
