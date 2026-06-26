## Description: <br>
Local ffmpeg and Pillow thumbnail generator for videos that picks candidate frames, composes thumbnails with text overlays and watermarks, ranks A/B variants with objective click-likelihood metrics, and exports common platform sizes without AI APIs or remote calls. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gopendrasharma89-tech](https://clawhub.ai/user/gopendrasharma89-tech) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External creators, developers, and operators use this skill to generate local video thumbnails, A/B variants, platform-specific exports, and JSON scoring reports without remote services. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Dependencies installed from untrusted sources could introduce local execution risk. <br>
Mitigation: Install ffmpeg, ffprobe, python3, and Pillow only from trusted package sources. <br>
Risk: Generated thumbnails or reports can overwrite existing files when the same output paths are reused. <br>
Mitigation: Run the scripts in a dedicated output directory and avoid reusing filenames for files that should be preserved. <br>
Risk: Frame ranking and click-likelihood scores are heuristic and may not reflect audience response or semantic quality. <br>
Mitigation: Review selected frames and winning variants before publishing or using them for business decisions. <br>


## Reference(s): <br>
- [Openclaw Thumbnail Forge on ClawHub](https://clawhub.ai/gopendrasharma89-tech/openclaw-thumbnail-forge) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Guidance, Files, JSON] <br>
**Output Format:** [Markdown guidance with bash commands; generated PNG images and JSON reports when executed] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires local ffmpeg, ffprobe, python3, and Pillow; writes outputs to user-selected paths] <br>

## Skill Version(s): <br>
0.3.0 (source: server release metadata and SKILL.md) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
