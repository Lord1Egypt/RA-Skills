## Description:

Searches for movies, TV shows, or other content on magnet/torrent sites and uses browser automation to extract working magnet URLs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[scottzx](https://clawhub.ai/user/scottzx)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to locate magnet/torrent download links for named media or other content through browser-based search workflows. It should be used only for content the user is authorized to download.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill is designed to locate torrent and magnet links, which can create legal and security risk when used with unauthorized content or untrusted torrent-related sites.

Mitigation: Use it only for content the user is authorized to download and review the target site before following or sharing any magnet link.

Risk: The workflow asks users to install unpinned global browser tooling.

Mitigation: Pin and verify agent-browser before installation, and run browser automation in a low-privilege or isolated environment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/scottzx/skills/magnet-searcher)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown guidance with shell command examples and magnet URL strings]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include browser navigation steps, troubleshooting guidance, and extracted magnet links.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
