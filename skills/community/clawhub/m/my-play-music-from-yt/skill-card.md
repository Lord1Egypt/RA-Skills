## Description: <br>
Play music on YouTube through visible browser automation with playwright-cli, including searches for songs, artists, playlists, genres, and playback controls. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[whodidthese](https://clawhub.ai/user/whodidthese) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and agent operators use this skill to play and control YouTube music in a visible browser session. It helps choose appropriate YouTube results for specific songs, artist mixes, playlists, genres, and mood-based requests. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill controls a visible browser through playwright-cli. <br>
Mitigation: Install and run it only with a trusted local playwright-cli installation and review browser actions before granting operating system permissions. <br>
Risk: Persistent browser mode can retain YouTube or Google login state and other browser profile data on disk. <br>
Mitigation: Use a dedicated browser profile for this automation and run the documented close and delete-data cleanup when retained login state is no longer wanted. <br>
Risk: macOS may require Screen Recording, Automation, and Accessibility permissions for browser snapshots and control. <br>
Mitigation: Grant those permissions only for a trusted local playwright-cli setup, and avoid sensitive browsing in the same browser profile. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/whodidthese/my-play-music-from-yt) <br>
- [Playwright CLI command reference](references/playwright-ref.md) <br>
- [YouTube page element identification guide](references/youtube-guide.md) <br>
- [YouTube](https://www.youtube.com) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and concise status text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses a named visible playwright-cli browser session and may retain YouTube browser profile data when persistent mode is used.] <br>

## Skill Version(s): <br>
0.0.9 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
