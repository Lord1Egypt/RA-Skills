## Description: <br>
Spotify控制技能 - 终端控制Spotify播放、搜索、管理播放列表。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[534422530](https://clawhub.ai/user/534422530) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to control Spotify playback from a terminal, including play/pause, track navigation, search, playlist operations, current playback display, and volume changes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Playback, volume, or playlist changes may occur unintentionally if commands are run without clear user intent. <br>
Mitigation: Require explicit confirmation before issuing commands that change playback state, volume, or playlists. <br>
Risk: The required command-line tool may differ between metadata and examples. <br>
Mitigation: Verify the locally installed Spotify CLI and command syntax before running generated commands. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/534422530/laosi-spotify) <br>
- [Publisher profile](https://clawhub.ai/user/534422530) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash and Python code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include JSON-formatted Spotify status or search results when the local CLI returns structured output.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
