## Description: <br>
Generate Music on PoYo / poyo.ai via `https://api.poyo.ai/api/generate/submit`; use for `generate-music`, AI music generation, background tracks, soundtrack drafts, instrumental songs, custom mode, music callbacks, and music detail retrieval. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[coolhackboy](https://clawhub.ai/user/coolhackboy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to prepare PoYo music-generation payloads, choose simple or custom music mode, submit asynchronous tasks, and explain callback or result retrieval steps. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses POYO_API_KEY to call PoYo and submit prompts, lyrics, style details, callback URLs, and related task data to a third-party API. <br>
Mitigation: Keep POYO_API_KEY server-side in an environment variable or secret manager, avoid exposing it in browser code or logs, and review payload files before submission. <br>
Risk: Prepared payloads may include private prompts, lyrics, callback URLs, or generated audio URLs. <br>
Mitigation: Avoid logging private request data or generated URLs unless the product policy explicitly allows it. <br>


## Reference(s): <br>
- [PoYo Generate Music API Reference](references/api.md) <br>
- [PoYo Generate Music Documentation](https://docs.poyo.ai/api-manual/music-series/generate-music) <br>
- [PoYo Query Music Detail Documentation](https://docs.poyo.ai/api-manual/music-series/query-music-detail) <br>
- [PoYo Music Webhook Documentation](https://docs.poyo.ai/api-manual/music-series/music-webhook) <br>
- [PoYo Generate Music Model Page](https://poyo.ai/models/generate-music) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with JSON payloads and bash or curl examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include model choice, mode selection, instrumental or vocal intent, payload summary, task_id, and follow-up retrieval or webhook guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
