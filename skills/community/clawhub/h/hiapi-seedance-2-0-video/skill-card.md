## Description: <br>
Generate videos with HiAPI's seedance-2-0 model via the HiAPI unified async task API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hiapiai](https://clawhub.ai/user/hiapiai) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and external agent users use this skill to generate Seedance 2.0 text-to-video and image-to-video outputs through HiAPI, including first/last-frame and multimodal reference workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts, media URLs or data URIs, and generation settings may be sent to HiAPI with the user's API key. <br>
Mitigation: Use only trusted HiAPI endpoints and avoid submitting secrets or private media unless approved for that workflow. <br>
Risk: Generated videos may be saved locally under outputs/ or returned as remote URLs. <br>
Mitigation: Review output locations and remote links before sharing generated media outside the intended audience. <br>
Risk: The npx installer can replace an existing local copy of the skill folder. <br>
Mitigation: Back up locally modified skill files before running the installer. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/hiapiai/hiapi-seedance-2-0-video) <br>
- [HiAPI Documentation](https://docs.hiapi.ai) <br>
- [HiAPI Seedance 2.0 Video API](references/api.md) <br>
- [Output Handling](references/output.md) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, JSON, Files, Guidance] <br>
**Output Format:** [JSON with generated video file paths or remote URLs, plus concise Markdown guidance for setup and failures] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Downloads generated HTTP(S) videos to outputs/ when possible; otherwise returns the remote video URL.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
