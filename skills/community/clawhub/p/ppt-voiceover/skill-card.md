## Description:

Turns a page-separated slide script into per-slide voiceovers and SRT subtitles, a combined narration track, slide timings, and an ffmpeg image-concat list.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yanghhu](https://clawhub.ai/user/yanghhu)

### License/Terms of Use:

MIT

## Use Case:

External educators, trainers, and product teams use it to prepare voiceovers and subtitles for page-separated slide decks. They can use the timing data and concat list to assemble a narrated slide video.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release security assessment was benign with medium confidence, but the scan was partial, did not fully evidence the advertised slide-to-video workflow or verify tool permissions, and noted API calls may lack explicit timeouts.

Mitigation: Review the scripts and required permissions, test the local workflow with --dry-run, and supervise API-backed runs with an execution deadline.

Risk: Live voice generation requires a Miragea API key and may use account quotas or incur charges.

Mitigation: Keep MIRAGEA_API_KEY in an environment variable, do not share it, and check current capabilities and account limits before generation.

Risk: Reference-audio voice generation could use a voice without the speaker's authorization.

Mitigation: Use reference audio only when you have the speaker's permission.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yanghhu/skills/ppt-voiceover)
- [Miragea](https://miragea.ai)
- [Miragea API](https://miragea.ai/v1)

## Skill Output:

**Output Type(s):** [Audio files, Subtitle files, JSON, Text files, Shell commands]

**Output Format:** [WAV audio, SRT subtitles, JSON slide timings and manifests, and an ffmpeg concat text file]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [One narration stream per slide deck; dry-run creates silent placeholder audio. Live voice generation uses the Miragea API.]

## Skill Version(s):

1.0.0 (source: frontmatter, server release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
