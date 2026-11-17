## Description:

Picasso TikTok guides agents through a TikTok/Reels pipeline that writes scripts, generates TTS voiceover, creates a HeyGen talking avatar, transcribes subtitles with Whisper, composes 1080x1920 videos with ffmpeg, and can generate AI B-roll with Runway Gen-4.5.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pauldelavallaz](https://clawhub.ai/user/pauldelavallaz)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, social media operators, and developers use this skill to produce vertical TikTok or Instagram Reels videos from a topic, article, script, or source video. It is especially suited for workflows that need a reviewed Spanish-language script, generated voiceover, talking avatar, subtitles, layout selection, and final ffmpeg composition.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated voice audio, scripts, prompts, and media may be sent to external AI providers and a public file host.

Mitigation: Use only with content appropriate for those services, and replace the public uguu.se upload path with private expiring storage or an official HeyGen upload path before processing confidential voiceovers.

Risk: The workflow includes opinionated promotional script defaults that could introduce unwanted CTA or brand language.

Mitigation: Review and approve the generated script before audio generation, and remove unwanted CTA or brand phrasing before continuing.

## Reference(s):

- [Picasso TikTok ClawHub listing](https://clawhub.ai/pauldelavallaz/skills/picasso-tiktok)
- [ElevenLabs text-to-speech API](https://api.elevenlabs.io/v1/text-to-speech/$ELEVENLABS_VOICE_ID)
- [HeyGen video generation API](https://api.heygen.com/v2/video/generate)
- [OpenAI audio transcription API](https://api.openai.com/v1/audio/transcriptions)
- [Replicate Runway Gen-4.5 predictions API](https://api.replicate.com/v1/models/runwayml/gen-4.5/predictions)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python and shell command snippets plus generated media file instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces reviewed scripts, TTS variation guidance, avatar generation steps, subtitle correction guidance, ffmpeg composition commands, and final 1080x1920 H.264/AAC video settings.]

## Skill Version(s):

1.2.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
