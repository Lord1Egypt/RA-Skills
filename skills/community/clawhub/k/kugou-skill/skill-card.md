## Description:

酷狗 helps agents use the Kugou CLI to search music, get recommendations, view charts and listening history, manage favorites and playlists, adjust recommendation preferences, and control the local Kugou desktop client.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shamo88](https://clawhub.ai/user/shamo88)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to interact with Kugou Music through a global CLI for music discovery, account music data retrieval, playlist management, recommendation preference updates, and local desktop client playback control.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill relies on a globally installed npm CLI that can check for and apply updates.

Mitigation: Install only from a trusted npm publisher, review updates before applying them, and use the documented controls to disable update checks in restricted environments.

Risk: The skill can solicit and persist Kugou account login state, including base64 secrets.

Mitigation: Prefer QR login when possible, avoid pasting secrets into chat or shell history, and rotate or re-login if a secret may have been exposed.

Risk: The skill can read or change personal music account data and control the local Kugou client.

Mitigation: Confirm user intent before playlist, favorite, preference, or playback changes, and review command output before taking follow-up actions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/shamo88/skills/kugou-skill)
- [Authentication commands](artifact/references/auth.md)
- [Music commands](artifact/references/music.md)
- [Local client control commands](artifact/references/control.md)
- [Output format and display rules](artifact/references/output-format.md)
- [Error handling](artifact/references/error-handling.md)
- [Install commands](artifact/references/install.md)
- [Update commands](artifact/references/update.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and parsed JSON result summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill expects raw JSON from kugou-cli commands and converts results into concise user-facing music tables, links, status messages, and follow-up prompts.]

## Skill Version(s):

0.1.20 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
