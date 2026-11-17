## Description:

Controls JOOX web music playback through browser automation, including search, playback controls, charts, playlists, and login workflow guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhuoyitao](https://clawhub.ai/user/zhuoyitao)

### License/Terms of Use:


## Use Case:

External users use this skill to automate common JOOX web-player tasks: checking login state, searching for songs, starting playback, using player controls, and browsing charts or playlists.

### Deployment Geography for Use:

Global, with JOOX region settings documented for Hong Kong, Macau, Malaysia, Indonesia, and Thailand.

## Known Risks and Mitigations:

Risk: The skill stores reusable JOOX login state in a local joox-auth.json file.

Mitigation: Keep joox-auth.json private, exclude it from source control and synced folders, and remove it when it is no longer needed.

Risk: The skill lets an agent control a browser session that may be logged in to a JOOX account.

Mitigation: Review requested actions before running the skill and use it only with browser sessions and accounts intended for JOOX automation.

Risk: The skill includes an unverified personal email address in login support prompts.

Mitigation: Do not treat the listed email address as official JOOX support.

Risk: The skill depends on npm-installed browser automation tooling.

Mitigation: Pin and verify npm dependencies before installation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zhuoyitao/skills/joox-music-player)
- [JOOX web player](https://www.joox.com/hk)
- [JOOX charts](https://www.joox.com/hk/chart)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May use a local joox-auth.json browser state file for restoring a JOOX login session.]

## Skill Version(s):

0.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
