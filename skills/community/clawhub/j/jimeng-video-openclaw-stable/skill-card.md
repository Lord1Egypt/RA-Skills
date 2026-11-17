## Description:

Jimeng Video Stable guides an agent through a stable Jimeng video workflow: open the video page, submit generation, wait for completion, download the video locally, and verify the resulting file.

This skill is ready for commercial/non-commercial use.

## Publisher:

[haohao-ui](https://clawhub.ai/user/haohao-ui)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to operate Jimeng through an OpenClaw-managed browser profile when they need to generate videos, find the latest generated video, download an mp4, and report a verified local file path.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow may use an existing Jimeng browser session or profile.

Mitigation: Run it with the intended OpenClaw browser profile and review profile selection before submitting generation requests.

Risk: Video generation may run long or fail to complete.

Mitigation: Use the skill's bounded polling posture: check every 20-30 seconds, stop after 12 minutes, and report FAILED(timeout) instead of waiting indefinitely.

Risk: A downloaded video file may be missing, empty, or in an unexpected format.

Mitigation: Verify that the reported file exists, has nonzero size, and is an mp4 or the format declared by the page before using the result.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/haohao-ui/skills/jimeng-video-openclaw-stable)
- [Jimeng Video Tool](https://jimeng.jianying.com/ai-tool/home/?workspace=0&type=video)
- [Jimeng Asset Library](https://jimeng.jianying.com/ai-tool/asset)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance, files]

**Output Format:** [Markdown guidance with inline shell commands and final status text containing the local video path and verification result.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce a downloaded local video file and reports explicit FAILED states on timeout, submit, download, or verification failures.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
