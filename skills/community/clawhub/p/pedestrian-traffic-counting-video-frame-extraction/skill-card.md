## Description: <br>
Extract frames from video files and save them as images using OpenCV. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lnj22](https://clawhub.ai/user/lnj22) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to extract image frames from video files for video analysis, dataset preparation, thumbnails, object detection preprocessing, and related computer vision workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Large videos or small frame intervals can create many image files and consume significant disk space; reused output directories may also overwrite colliding frame filenames. <br>
Mitigation: Use a dedicated empty output directory, check available disk space before extraction, and choose an interval or frame range appropriate to the video size. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lnj22/pedestrian-traffic-counting-video-frame-extraction) <br>
- [Publisher profile](https://clawhub.ai/user/lnj22) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Python/OpenCV code examples and a JSON result schema.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated frame image files are written to the user-selected output directory when the described extraction code is run.] <br>

## Skill Version(s): <br>
0.1.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
