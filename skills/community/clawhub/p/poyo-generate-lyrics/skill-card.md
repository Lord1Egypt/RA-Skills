## Description:

Generate song lyrics on PoYo / poyo.ai via `https://api.poyo.ai/api/generate/submit`; use for `generate-lyrics`, lyric drafts, verses and choruses, theme-based songwriting, mood or genre guidance, music-generation preparation, callbacks, and music detail retrieval.

This skill is ready for commercial/non-commercial use.

## Publisher:

[coolhackboy](https://clawhub.ai/user/coolhackboy)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to prepare and submit PoYo generate-lyrics requests from a theme, mood, genre, or story direction, then retrieve or route draft lyric text for music-generation workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts, callback URLs, and draft lyrics in payloads are shared with PoYo during live API calls.

Mitigation: Review payload files before submission, avoid confidential or private content unless sharing with PoYo is acceptable, and make live calls only after explicit user approval in a trusted environment.

Risk: POYO_API_KEY exposure could allow unauthorized API use.

Mitigation: Keep POYO_API_KEY server-side and out of browser code, repositories, logs, screenshots, and chat output.

Risk: Generated lyrics may need originality, rights, and policy review before publication.

Mitigation: Treat returned lyrics as drafts and review them before publishing or passing them into downstream music-generation workflows.

## Reference(s):

- [PoYo Generate Lyrics API Reference](references/api.md)
- [PoYo Generate Lyrics Model Page](https://poyo.ai/models/generate-lyrics)
- [PoYo Generate Lyrics API Docs](https://docs.poyo.ai/api-manual/music-series/generate-lyrics)
- [PoYo Query Music Detail API Docs](https://docs.poyo.ai/api-manual/music-series/query-music-detail)
- [PoYo Music Webhook Docs](https://docs.poyo.ai/api-manual/music-series/music-webhook)
- [ClawHub Skill Page](https://clawhub.ai/coolhackboy/skills/poyo-generate-lyrics)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with JSON payload examples and bash commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires POYO_API_KEY; live API calls submit reviewed prompt or payload data to PoYo and may return an asynchronous task_id.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
