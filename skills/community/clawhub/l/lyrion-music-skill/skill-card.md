## Description: <br>
Controls Lyrion Music Server (LMS) through its JSON-RPC API for playback, volume, playlist, player, and music library operations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[photonixlaser-ux](https://clawhub.ai/user/photonixlaser-ux) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to let an agent inspect and control a reachable Lyrion Music Server, including playback state, volume, playlists, player selection, and music database search. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Commands can change playback, volume, power state, and playlist contents on the configured audio setup. <br>
Mitigation: Review commands before execution, especially power, volume, playlist add, and playlist clear operations. <br>
Risk: A misconfigured host or port could send control commands to an unintended Lyrion Music Server. <br>
Mitigation: Set LYRION_HOST and LYRION_PORT explicitly before use so the agent targets the intended server. <br>


## Reference(s): <br>
- [Lyrion Music Server API Reference](references/api.md) <br>
- [Lyrion CLI Reference](https://lyrion.org/reference/cli/) <br>
- [LMS Community slimserver](https://github.com/LMS-Community/slimserver) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, API calls, Configuration, Guidance] <br>
**Output Format:** [Shell commands and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a reachable Lyrion Music Server and a valid player ID for player-specific commands.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
