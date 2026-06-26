## Description: <br>
Generate images, videos, speech audio, and music using the PonyFlash Python SDK, and handle local media editing with FFmpeg for clipping, concatenation, transcoding, audio extraction, frame capture, subtitle checks, and ASS subtitle preparation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[leothebravest](https://clawhub.ai/user/leothebravest) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and creative operators use this skill to route agent requests between PonyFlash cloud media generation and local FFmpeg-based editing workflows. It supports end-to-end production tasks such as generating image, video, speech, or music assets, then trimming, combining, transcoding, subtitling, or exporting final media. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses PonyFlash as a cloud media processor, so prompts, uploaded media, and generated assets may leave the local machine during cloud generation tasks. <br>
Mitigation: Use the skill only with media and prompts suitable for PonyFlash processing, and avoid sensitive photos, audio, videos, brand assets, or confidential prompts unless the data-handling implications are acceptable. <br>
Risk: The artifact asks users to provide a live PonyFlash API key in chat for cloud generation tasks. <br>
Mitigation: Do not paste API keys into chat; provide PONYFLASH_API_KEY through a secure environment variable or secret manager. <br>
Risk: Cloud generation can consume account credits and may incur unexpected cost when running expensive generation steps. <br>
Mitigation: Verify account credits and review generation choices before executing costly image, video, speech, or music requests. <br>
Risk: Local FFmpeg workflows can overwrite, transcode, or transform user media if commands are run against the wrong paths or formats. <br>
Mitigation: Use temporary task directories for intermediates, avoid overwriting outputs unless explicitly allowed, and validate final media before cleanup. <br>


## Reference(s): <br>
- [PonyFlash ClawHub Release](https://clawhub.ai/leothebravest/ponyflash) <br>
- [PonyFlash Publisher Profile](https://clawhub.ai/user/leothebravest) <br>
- [PonyFlash Website](https://www.ponyflash.com) <br>
- [Models Reference](reference/models.md) <br>
- [Image Generation Reference](reference/images.md) <br>
- [Video Generation Reference](reference/video.md) <br>
- [Speech Generation Reference](reference/speech.md) <br>
- [Music Generation Reference](reference/music.md) <br>
- [Local Media Operations Reference](reference/operations.md) <br>
- [Examples Reference](reference/examples.md) <br>
- [Creative Playbooks Index](playbooks/INDEX.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with inline Python and shell command blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce cloud generation requests and local media-processing command plans; final media files are task outputs when the agent executes the generated workflow.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata; artifact frontmatter reports 0.3.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
