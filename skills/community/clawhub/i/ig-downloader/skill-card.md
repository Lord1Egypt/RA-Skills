## Description:

Download Instagram profile media (reels MP4, photos JPG, full carousel multi-image JPG) via sessionid (instagrapi), Apify dataset fallback, or interactive setup wizard.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cripterhack](https://clawhub.ai/user/cripterhack)

### License/Terms of Use:

GPL-2.0

## Use Case:

Developers and external users use this skill to guide an agent through installing and running an Instagram media downloader with session-cookie setup, direct sessionid use, or Apify dataset fallback.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The downloader uses an Instagram session cookie, which can grant account access if exposed.

Mitigation: Use a non-sensitive account where possible, avoid passing sessionid values on the command line, and delete ~/.ig-downloader/config.json or settings.json when finished.

Risk: One-line remote installers can install code and agent files broadly before local review.

Mitigation: Prefer cloning a tagged release, inspecting the files, and then installing from the reviewed local copy.

Risk: Apify or toon input data can control download URLs and output names.

Mitigation: Process only trusted dataset exports and review generated paths before using downloaded output.

## Reference(s):

- [ClawHub Skill Listing](https://clawhub.ai/cripterhack/skills/ig-downloader)
- [instagrapi](https://github.com/subzeroid/instagrapi)
- [Python Downloads](https://www.python.org/downloads/)
- [skills.sh Listing](https://skills.sh/cripterhack/ig-downloader-skill)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, Files]

**Output Format:** [Markdown guidance with CLI commands; JPG, MP4, and text files when the downloader is executed]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Downloads are organized into dated profile media folders with post_info.txt metadata unless flat output is requested.]

## Skill Version(s):

2.2.0 (source: ClawHub release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
