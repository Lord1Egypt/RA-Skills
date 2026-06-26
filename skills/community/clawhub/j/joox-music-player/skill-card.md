## Description: <br>
Control JOOX music playback via web browser automation, including searching songs, artists, albums, and playlists, playing music, controlling playback, browsing charts, and managing playlists. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ZhuoYitao](https://clawhub.ai/user/ZhuoYitao) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and agents use this skill to operate the JOOX web player through browser automation for music search, playback, chart browsing, playlist navigation, and playback controls. <br>

### Deployment Geography for Use: <br>
Hong Kong, Macau, Malaysia, Indonesia, and Thailand content regions; availability remains subject to JOOX regional catalog access. <br>

## Known Risks and Mitigations: <br>
Risk: Browser automation can use a user's JOOX account and saved login state. <br>
Mitigation: Install only when account automation is acceptable, keep joox-auth.json private, and delete the saved session file when it is no longer needed. <br>
Risk: Setup commands install npm and Playwright components before use. <br>
Mitigation: Review the npm and Playwright commands before running them in the target environment. <br>
Risk: The artifact includes an unofficial support email. <br>
Mitigation: Do not send credentials or account details to the support email shown in the skill. <br>


## Reference(s): <br>
- [JOOX Web Player](https://www.joox.com/hk) <br>
- [JOOX Charts](https://www.joox.com/hk/chart) <br>
- [ClawHub Skill Page](https://clawhub.ai/ZhuoYitao/joox-music-player) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration instructions] <br>
**Output Format:** [Markdown with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May guide browser automation steps and saved login-state handling for joox-auth.json.] <br>

## Skill Version(s): <br>
0.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
