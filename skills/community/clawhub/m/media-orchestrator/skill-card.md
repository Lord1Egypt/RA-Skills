## Description: <br>
Unified skill for resolving, downloading, and delivering media (audio/video) to chat platforms. Integrates yt-dlp for resolution and handles Spotify metadata sync. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sieershafilone](https://clawhub.ai/user/sieershafilone) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and agent operators use this skill to resolve requested audio, video, or Spotify media, download it into the OpenClaw workspace, and deliver the resulting file or playback metadata through WhatsApp or Telegram workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill downloads requested media into the OpenClaw workspace, which can leave private, copyrighted, or large files on disk. <br>
Mitigation: Confirm media requests before execution, monitor workspace storage, and periodically remove downloaded files because the evidence does not show automatic deletion or file-size limits. <br>
Risk: The skill can send resulting files through configured WhatsApp or Telegram accounts. <br>
Mitigation: Confirm the intended recipient and chat target before sending any media file. <br>
Risk: The workflow depends on local media tooling and configured chat integrations. <br>
Mitigation: Install and verify required tools and account integrations in the target environment before relying on the skill for delivery. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/sieershafilone/media-orchestrator) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, code] <br>
**Output Format:** [Agent guidance with local command execution and generated media or JSON files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May download media files into the OpenClaw workspace and send files through configured WhatsApp or Telegram accounts.] <br>

## Skill Version(s): <br>
0.1.1 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
