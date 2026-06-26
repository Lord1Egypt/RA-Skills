## Description: <br>
This skill handles Spotify requests that read, create, update, or delete Spotify data through the OOMOL `oo` CLI connector. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to search Spotify, inspect account and catalog data, manage playlists and saved library items, and control playback from an OOMOL-connected Spotify account. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can perform Spotify write actions that change playlists, saved library items, playback state, follows, queue, and device settings. <br>
Mitigation: Confirm the exact payload and intended effect with the user before running actions tagged as write. <br>
Risk: The skill can perform destructive actions that remove or overwrite Spotify data. <br>
Mitigation: Require explicit approval for the target and action before running commands tagged as destructive. <br>
Risk: Connector actions depend on account authentication, scopes, app readiness, and OOMOL account credit. <br>
Mitigation: Use first-time setup and connection recovery steps only after a command fails for the matching reason. <br>


## Reference(s): <br>
- [Spotify homepage](https://spotify.com) <br>
- [oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [oo CLI install guide](https://cli.oomol.com/install-guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON payload examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses live connector schemas before constructing action payloads.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
