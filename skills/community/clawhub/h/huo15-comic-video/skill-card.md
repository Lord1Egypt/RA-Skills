## Description: <br>
Generates short vertical video clips from storyboard key frames using Volcengine Ark Seedance 2.0 image-to-video, with 5-second scenes, up to three concurrent jobs, and last-frame outputs for scene continuity. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhaobod1](https://clawhub.ai/user/zhaobod1) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Creators, developers, and production agents use this skill to turn prepared comic storyboard frames and scene metadata into short MP4 video clips for vertical comic-drama workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a Volcengine Ark API key and sends storyboard frames and prompts to the provider. <br>
Mitigation: Use a scoped API key, review the selected frames and prompts before execution, and avoid processing sensitive material unless the provider terms and data handling are acceptable. <br>
Risk: Video generation can incur paid provider charges, and local cost tracking records charges after jobs complete. <br>
Mitigation: Set provider-side spending limits, review the requested scene count and resolution, and keep the skill's lower-resolution or fast-mode options in mind when controlling cost. <br>
Risk: Incorrect input or output paths could upload unintended frames or overwrite expected generated media. <br>
Mitigation: Review the script path, frame directory, and output directory before running the command. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/zhaobod1/huo15-comic-video) <br>
- [Volcengine Seedance documentation](https://www.volcengine.com/docs/82379/1520757) <br>


## Skill Output: <br>
**Output Type(s):** [Files, Shell commands, Configuration instructions] <br>
**Output Format:** [MP4 video files, PNG last-frame files, checkpoint metadata, and console status output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces one MP4 per scene plus optional last-frame PNGs for continuity; uses ARK_API_KEY and paid provider API calls.] <br>

## Skill Version(s): <br>
0.1.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
