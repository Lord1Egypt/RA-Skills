## Description: <br>
Generate thumbnails from videos. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jpengcheng523-netizen](https://clawhub.ai/user/jpengcheng523-netizen) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and automation users use this skill to generate video thumbnails through a command-line workflow and receive JSON results. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The referenced scripts/video_thumbnail.py file is not included in the artifact, so its behavior cannot be reviewed from the provided release files. <br>
Mitigation: Review the script source separately before installing or running the skill. <br>
Risk: The skill requires THUMBNAIL_API_KEY, but the service and handling requirements are under-documented. <br>
Mitigation: Set the key only for a known service, keep it out of commits and logs, and rotate it if exposure is suspected. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jpengcheng523-netizen/jpeng-video-thumbnail) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/jpengcheng523-netizen) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, JSON, Guidance] <br>
**Output Format:** [Markdown with bash commands and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires THUMBNAIL_API_KEY and references an external video_thumbnail.py script that is not included in the artifact.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
