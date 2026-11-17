## Description:

Automatically fetches Douyin videos from short, standard, or share links by extracting the video ID and downloading through a simulated iPhone browser.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ly5201314gjx](https://clawhub.ai/user/ly5201314gjx)

### License/Terms of Use:


## Use Case:

Developers and operators use lgCapture to download Douyin videos from supported Douyin link formats in a CLI workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Loose URL validation may cause the downloader to contact unintended internal or attacker-controlled addresses.

Mitigation: Use only trusted Douyin links, avoid arbitrary or shortened links from untrusted sources, and run the skill in a network-restricted environment when possible.

Risk: download.py can write to a caller-selected output path.

Mitigation: Review output paths before execution and keep downloads in a controlled directory.

## Reference(s):

- [ClawHub lgCapture skill page](https://clawhub.ai/ly5201314gjx/skills/lgcapture)

## Skill Output:

**Output Type(s):** [Shell commands, Files, Text]

**Output Format:** [CLI output with a downloaded MP4 file path]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes downloaded videos to /tmp by default; download.py can also write to a caller-selected output path.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
