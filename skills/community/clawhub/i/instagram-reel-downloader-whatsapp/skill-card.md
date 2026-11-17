## Description:

Download an Instagram Reel via sssinstagram.com and return it as a WhatsApp-ready video file.

This skill is ready for commercial/non-commercial use.

## Publisher:

[besaif](https://clawhub.ai/user/besaif)

### License/Terms of Use:


## Use Case:

External users and assistants use this skill to download a provided Instagram Reel through sssinstagram.com and return the resulting video file for WhatsApp delivery.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Reel URLs are sent to sssinstagram.com, a third-party downloader site.

Mitigation: Use the skill only when sharing the Reel URL with that service is acceptable.

Risk: The workflow runs browser automation in a no-sandbox browser configuration.

Mitigation: Run it in an isolated container or unprivileged account with no secrets and restricted network access.

Risk: Downloaded media is accepted from third-party links discovered during automation.

Mitigation: Use a dedicated output directory, review downloaded files before reuse, and run cleanup after completion.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/besaif/skills/instagram-reel-downloader-whatsapp)
- [sssinstagram Reels downloader](https://sssinstagram.com/reels-downloader)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance, files]

**Output Format:** [Plain text status, MEDIA_PATH output, and a downloaded video file]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js 18+, playwright-core, a Chromium-compatible browser, and network access to Instagram and sssinstagram.com.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
