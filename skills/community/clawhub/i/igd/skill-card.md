## Description:

Download Instagram profile media (reels MP4, photos JPG, full carousel multi-image JPG) via sessionid (instagrapi), Apify dataset fallback, or interactive setup wizard.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cripterhack](https://clawhub.ai/user/cripterhack)

### License/Terms of Use:

GPL-2.0-only

## Use Case:

External users and developers use this skill to guide an agent through installing and running an Instagram media downloader with session-cookie, setup-wizard, or Apify dataset workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles Instagram session cookies and can save credentials under ~/.ig-downloader.

Mitigation: Use a dedicated or least-privileged Instagram account, avoid passing cookies or API tokens on the command line, and remove ~/.ig-downloader credentials when done.

Risk: Installer documentation includes curl|bash and PowerShell iex patterns.

Mitigation: Prefer reviewing and running from a pinned source checkout before installing.

Risk: Apify/toon dataset inputs and downloaded media URLs may be untrusted.

Mitigation: Avoid untrusted datasets until URL and path validation are confirmed, and download into a controlled output directory.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cripterhack/skills/igd)
- [ClawHub publisher profile](https://clawhub.ai/user/cripterhack)
- [instagrapi project](https://github.com/subzeroid/instagrapi)
- [Python downloads](https://www.python.org/downloads/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and configuration steps]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May recommend commands that create local media downloads and save Instagram session configuration when the user runs the tool.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata; artifact source files declare 2.2.0/2.3.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
