## Description: <br>
Control NetEase Cloud Music Web in a browser to search and play songs by keyword or open My Music and play one of the user's own created playlists by keyword. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yangyunzhao](https://clawhub.ai/user/yangyunzhao) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and music listeners use this skill to have an agent operate NetEase Cloud Music Web for song search playback or playback from their own created playlists in My Music. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The agent may interact with a logged-in NetEase Cloud Music Web account and view playlist names while playing My Music playlists. <br>
Mitigation: Install only if browser control in that account is acceptable; supervise first runs and keep use limited to song or playlist playback. <br>
Risk: Ambiguous short song searches may select the wrong track. <br>
Mitigation: Prefer artist plus song title and ask for confirmation when multiple matches are plausible. <br>
Risk: Browser clicks near playback controls may hit adjacent options such as MV playback or client prompts. <br>
Mitigation: Avoid MV and client-playback controls, wait briefly after clicking play, and verify that the bottom player switched to the target before reporting success. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Text] <br>
**Output Format:** [Natural-language browser-control guidance and status updates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Instruction-driven browser interaction; no executable helper code in the current release.] <br>

## Skill Version(s): <br>
0.1.6 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
