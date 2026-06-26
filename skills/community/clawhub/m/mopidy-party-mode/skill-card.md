## Description: <br>
Run a Mopidy music system in party mode for shared or group chats, where everyone can contribute songs but only the host can control playback. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[grantmacnamara](https://clawhub.ai/user/grantmacnamara) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and hosts use this skill to let party guests search music, inspect playback state, and add tracks, albums, playlists, or locally matched ranked requests to a Mopidy queue while reserving playback controls for the host. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Guests may request playback-changing actions such as play, pause, skip, clear, or play-track. <br>
Mitigation: Require explicit host approval before running host-only playback controls. <br>
Risk: Open group chats may make it difficult to distinguish host requests from guest requests. <br>
Mitigation: Install only where host identity is reliable, or separate host controls from guest-safe queue actions. <br>
Risk: Backend-specific Mopidy library behavior and URI schemes may vary by installation. <br>
Mitigation: Confirm supported Mopidy methods and URI schemes against the target server before relying on backend-specific behavior. <br>


## Reference(s): <br>
- [Mopidy API Notes](references/api-notes.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/grantmacnamara/mopidy-party-mode) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and concise user-facing text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses Mopidy JSON-RPC through a configured MOPIDY_URL endpoint and requires curl, jq, and python3.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
