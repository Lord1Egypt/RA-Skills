## Description: <br>
Download media into /mnt/jellyfin_media subfolders and track progress. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[vivek9patel](https://clawhub.ai/user/vivek9patel) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and media-library operators use this skill to confirm a destination folder, download user-provided media URLs into a mounted library, and check download progress. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill writes downloaded media into /mnt/jellyfin_media. <br>
Mitigation: Mount only the intended media library at /mnt/jellyfin_media and confirm the destination folder before allowing downloads. <br>
Risk: Progress files in /tmp may expose private or tokenized media URLs on shared machines. <br>
Mitigation: Use controlled temporary-file access and avoid private or tokenized URLs in shared environments. <br>
Risk: User-provided URLs are downloaded by yt-dlp into the configured media folder. <br>
Mitigation: Review links before confirming the download and keep yt-dlp available from a trusted installation source. <br>


## Reference(s): <br>
- [Media Sync on ClawHub](https://clawhub.ai/vivek9patel/media-sync) <br>
- [OpenClaw](https://openclaw.ai) <br>
- [yt-dlp](https://github.com/yt-dlp/yt-dlp) <br>
- [Jellyfin](https://jellyfin.org) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Files, Configuration, Guidance] <br>
**Output Format:** [Concise text with structured tool-status summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses OpenClaw tool calls to validate folders, start batched downloads, and report progress.] <br>

## Skill Version(s): <br>
1.1.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
