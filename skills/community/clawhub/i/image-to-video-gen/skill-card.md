## Description: <br>
Generates short videos from supplied images by using Gemini Vision to analyze the image and Google's Veo 3.0 API to create and download an MP4. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[j3ffyang](https://clawhub.ai/user/j3ffyang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, media creators, and agent operators use this skill to turn local or URL images into short cinematic MP4 videos with saved prompts and intermediate files for review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Images and prompts are uploaded to Google services. <br>
Mitigation: Avoid confidential, personal, or regulated images unless that sharing is acceptable for the intended use. <br>
Risk: Generated videos and intermediate prompt files are retained locally under ~/.openclaw/workspace/tibetanProc/. <br>
Mitigation: Review and clean the output directory when local retention is no longer needed. <br>
Risk: The workflow depends on a GOOGLE_API_KEY for Google API calls. <br>
Mitigation: Configure the key through the environment and avoid embedding credentials in prompts, files, or shared logs. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/j3ffyang/image-to-video-gen) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, code, shell commands, configuration, files] <br>
**Output Format:** [Markdown with Python and shell code blocks; generated workflow outputs include MP4 video, prompt text or Markdown, and JSON API responses.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires GOOGLE_API_KEY and writes timestamped artifacts under ~/.openclaw/workspace/tibetanProc/.] <br>

## Skill Version(s): <br>
3.0.0 (source: release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
