## Description:

Download YouTube videos and upload them to Pocket Casts Files for offline viewing. For personal use with content you own or have rights to.

This skill is ready for commercial/non-commercial use.

## Publisher:

[manuelhettich](https://clawhub.ai/user/manuelhettich)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to prepare a YouTube URL for offline viewing by downloading it, converting it to MP4, and uploading it to Pocket Casts Files. It is intended for personal use with media the user owns or has rights to download and upload.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow stores a long-lived Pocket Casts refresh token and YouTube cookies locally.

Mitigation: Keep the credentials directory permission-restricted, avoid sharing logs or local files, and rotate or revoke credentials if exposure is suspected.

Risk: The workflow runs unpinned external runtime tools with access to local credentials.

Mitigation: Review or pin external tools before use and do not run the script with elevated privileges.

Risk: Downloading or uploading media without the necessary rights may violate terms of service or copyright law.

Mitigation: Use the skill only with personal recordings, Creative Commons media, user-created videos, or content where downloading and uploading are permitted.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/manuelhettich/skills/pocket-casts-yt)
- [Publisher profile](https://clawhub.ai/user/manuelhettich)
- [Pocket Casts](https://pocketcasts.com)
- [Deno install script](https://deno.land/install.sh)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The runtime workflow creates and removes a temporary MP4 file and prints upload status plus the Pocket Casts file UUID.]

## Skill Version(s):

1.0.0 (source: server release metadata and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
