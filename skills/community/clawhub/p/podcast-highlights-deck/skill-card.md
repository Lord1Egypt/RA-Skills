## Description:

Creates a highly visual editorial long-scroll HTML microsite from a podcast episode with 8-12 curated highlights, playable original audio clips, multilingual UI and content, and a sticky table-of-contents rail.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ken-chy129](https://clawhub.ai/user/ken-chy129)

### License/Terms of Use:

MIT-0

## Use Case:

Content teams, podcasters, and developers use this skill to turn a podcast episode URL into a polished static highlights site. It is intended for workflows that need curated episode moments, original audio clips, translated UI and content, and an editorial reading experience rather than a full transcript.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow downloads and processes podcast or video audio, which may be copyrighted or subject to platform restrictions.

Mitigation: Use the skill only with episodes the user has rights to process, and validate source URLs before publishing the generated site.

Risk: The workflow may contact RSS, podcast, video, transcription, and font services, and the fallback transcription path may send audio to an external API.

Mitigation: Confirm acceptable network and external API use before execution, especially when source audio could contain sensitive or non-public material.

Risk: The clipping helper has a small path-validation weakness around highlight IDs used to create audio filenames.

Mitigation: Keep generated highlight IDs simple, such as h1 through h12, and inspect generated clip paths before bundling or publishing.

Risk: Automated transcripts and translations can introduce quote, timing, or meaning errors in the published highlight deck.

Mitigation: Review selected quotes, timestamps, translations, and takeaways against the source transcript or audio before distribution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ken-chy129/skills/podcast-highlights-deck)
- [Skill README](artifact/README.md)
- [Skill workflow](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, files]

**Output Format:** [Static website bundle with JSON content, React/CSS template files, generated audio clips, and concise Markdown or shell-command guidance during execution]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces curated highlights rather than a full transcript, with multilingual UI/content and per-highlight original audio playback.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
