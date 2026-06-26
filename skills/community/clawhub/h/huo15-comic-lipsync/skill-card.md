## Description: <br>
Synchronizes video shots with dialogue audio using Kling lip sync, and skips shots that have no dialogue audio. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhaobod1](https://clawhub.ai/user/zhaobod1) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and video-production agents use this skill to batch-process scene videos and dialogue audio into lip-synced MP4 outputs for comic or short-form video workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Selected video clips and dialogue audio are sent to Kling for processing and may incur API costs. <br>
Mitigation: Use a dedicated KLING_API_KEY where possible, test on a small directory first, and confirm expected cost before processing a larger batch. <br>
Risk: The security guidance notes that the documented --no-lipsync option is not implemented by the included script. <br>
Mitigation: Do not rely on --no-lipsync for cost control; limit input size, use the cost guard behavior, or skip running the script when lip sync is not needed. <br>


## Reference(s): <br>
- [Kling lip-sync API endpoint](https://api.kling.com/v1/videos/lip-sync) <br>
- [Kling API base used by script](https://api.klingai.com/v1) <br>


## Skill Output: <br>
**Output Type(s):** [Files, Shell commands, Guidance] <br>
**Output Format:** [MP4 video files plus terminal status text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires KLING_API_KEY; videos without dialogue audio are copied to the output directory unchanged.] <br>

## Skill Version(s): <br>
0.1.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
