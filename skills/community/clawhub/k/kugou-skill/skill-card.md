## Description: <br>
Provides Kugou Music song search, personalized and similar recommendations, favorites, listening statistics, charts, and playlist creation through the kugou-cli tool. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shamo88](https://clawhub.ai/user/shamo88) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to install and operate a Kugou Music CLI for music search, recommendations, charts, account-linked collections, listening statistics, and user-confirmed playlist creation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can handle a persistent Kugou account secret and store it in ~/.config/kugou-cli/auth.json. <br>
Mitigation: Prefer QR login over pasting a base64 secret into chat; treat any secret as an account credential and avoid using it on shared machines. <br>
Risk: The artifact gives inconsistent guidance about whether npm @latest installs can happen automatically. <br>
Mitigation: Disable automatic update checks with --no-update-check or KUGOU_CLI_NO_UPDATE_CHECK=1, or verify update behavior before routine use. <br>
Risk: Playlist creation modifies a user's Kugou account. <br>
Mitigation: Create playlists only after the user explicitly asks or confirms that the current song set should be saved. <br>


## Reference(s): <br>
- [ClawHub package page](https://clawhub.ai/shamo88/kugou-skill) <br>
- [Authentication commands](references/auth.md) <br>
- [Music commands](references/music.md) <br>
- [Output format and presentation rules](references/output-format.md) <br>
- [Update commands](references/update.md) <br>
- [Error handling](references/error-handling.md) <br>
- [Install commands](references/install.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, JSON, Markdown] <br>
**Output Format:** [Markdown guidance with shell commands and parsed JSON results, including Markdown links for song playback URLs.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands write JSON to stdout and errors to stderr; most music commands require login.] <br>

## Skill Version(s): <br>
0.1.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
