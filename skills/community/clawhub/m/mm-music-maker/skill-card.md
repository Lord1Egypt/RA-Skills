## Description: <br>
Create music with MiniMax music models, including songs or instrumental tracks from lyrics and style prompts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[BLUE-coconut](https://clawhub.ai/user/BLUE-coconut) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and creators use this skill to generate songs, instrumental music, or melodic chanting through the MiniMax Music Generation API and save the resulting audio locally or retrieve a temporary download URL. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Lyrics, prompts, and style details are sent to MiniMax for processing. <br>
Mitigation: Avoid submitting confidential, unpublished, or sensitive material unless third-party processing is acceptable. <br>
Risk: The skill requires a MiniMax API key. <br>
Mitigation: Provide the key through the MINIMAX_MUSIC_API_KEY environment variable and do not place credentials in prompts, logs, or committed files. <br>
Risk: Generated audio is written to a user-selected output path. <br>
Mitigation: Use ordinary workspace output paths and review generated files before sharing or relying on them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/BLUE-coconut/mm-music-maker) <br>
- [MiniMax Music Generation API](https://platform.minimaxi.com/docs/api-reference/music-generation) <br>
- [MiniMax API reference file](references/minimax_music_api.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, Files] <br>
**Output Format:** [Markdown guidance with inline bash commands; generated audio is saved as a local file or returned as a temporary URL when the script is run.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires MINIMAX_MUSIC_API_KEY. The MiniMax URL output option expires after 24 hours.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
