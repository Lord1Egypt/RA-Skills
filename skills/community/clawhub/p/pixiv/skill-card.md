## Description:

Pixiv Skill helps an agent retrieve Pixiv rankings, search illustrations, cache artwork metadata, download selected works, and perform authenticated Pixiv interactions such as like, follow, and artist monitoring.

This skill is ready for commercial/non-commercial use.

## Publisher:

[firstmeet1108](https://clawhub.ai/user/firstmeet1108)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to guide an agent through Pixiv ranking lookup, keyword search, metadata caching, cache review, and explicit artwork download workflows. The skill can also support authenticated Pixiv account actions when the user intends to like, follow, or monitor artists.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Pixiv cookies or OAuth tokens could be exposed if config.yaml is stored in a shared repository or broad workspace.

Mitigation: Treat config.yaml as a secret file, keep it out of shared repositories, and use restrictive local file permissions.

Risk: OAuth bearer tokens may be exposed during image download requests.

Mitigation: Review the authentication and download flow before use, and avoid sending bearer tokens to image hosts unless the behavior has been corrected.

Risk: Like, follow, download, and monitor commands can perform authenticated Pixiv account actions.

Mitigation: Run these commands only after explicit user confirmation and only with an account intended for those actions.

Risk: Unpinned dependencies can change behavior across installations.

Mitigation: Pin and review dependencies before deploying this skill in a controlled environment.

## Reference(s):

- [ClawHub Pixiv Skill Release Page](https://clawhub.ai/firstmeet1108/skills/pixiv)
- [Pixiv](https://www.pixiv.net/)
- [Pixiv Ranking Endpoint](https://www.pixiv.net/ranking.php)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance, files]

**Output Format:** [Markdown guidance with inline shell commands, plus JSON cache files and downloaded image files when requested]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Default workflows cache metadata before downloading; authenticated actions depend on local Pixiv credentials in config.yaml.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
