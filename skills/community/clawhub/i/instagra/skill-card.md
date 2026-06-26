## Description: <br>
Download an Instagram Reel via sssinstagram.com and return it as a WhatsApp-ready video file. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[TNjo](https://clawhub.ai/user/TNjo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to download a provided public Instagram Reel through sssinstagram.com and send the resulting video as WhatsApp-ready media. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Reel URLs are shared with sssinstagram.com and the downloaded media may be sent through WhatsApp. <br>
Mitigation: Use only links suitable for those services and avoid private or sensitive links unless the user trusts the services involved. <br>
Risk: Downloaded video files can remain in the configured download directory after use. <br>
Mitigation: Review the download location and run the cleanup script or delete files after the transfer is complete. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/TNjo/instagra) <br>
- [sssinstagram Reels downloader](https://sssinstagram.com/reels-downloader) <br>
- [Instagram](https://www.instagram.com/) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Files, Guidance] <br>
**Output Format:** [Shell command guidance plus a MEDIA_PATH string for a downloaded video file] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces a WhatsApp-ready video file and emits its absolute path as MEDIA_PATH.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
