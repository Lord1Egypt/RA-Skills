## Description:

Download an Instagram Reel via sssinstagram.com and return it as a WhatsApp-ready video file.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tnjo](https://clawhub.ai/user/tnjo)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to fetch an Instagram Reel through sssinstagram.com and prepare the downloaded video for WhatsApp delivery.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends Instagram Reel URLs to sssinstagram.com and automates a browser against third-party web content.

Mitigation: Use it only when that third-party processing is acceptable, and run it in a restricted workspace or container.

Risk: Downloaded media and browser automation could expose the runtime to unsafe files or unwanted network reachability.

Mitigation: Limit network access, restrict access to sensitive internal services, and apply disk quotas or cleanup for downloaded files.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tnjo/skills/instagra)
- [Publisher profile](https://clawhub.ai/user/tnjo)
- [sssinstagram Reel Downloader](https://sssinstagram.com/reels-downloader)

## Skill Output:

**Output Type(s):** [text, shell commands, files, guidance]

**Output Format:** [Plain text instructions and shell commands that produce a local video file path]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The primary runtime result is MEDIA_PATH pointing to a downloaded video file.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
