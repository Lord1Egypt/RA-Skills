## Description: <br>
Generates podcast-style MP3 audio from one or more URLs, articles, videos, or PDFs using Podcastfy with Gemini transcript generation and Edge TTS speech synthesis. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[watermelon11](https://clawhub.ai/user/watermelon11) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to generate podcast-style MP3 summaries from one or more acceptable URLs in Clawdbot workflows, including scheduled jobs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill downloads Python packages and Playwright Chromium at runtime. <br>
Mitigation: Pin or pre-provision dependencies in stricter environments before deploying the skill. <br>
Risk: URL-derived content is processed by external services through Gemini and Edge TTS. <br>
Mitigation: Use only public or approved URLs, and avoid private or internal URLs unless those data flows are acceptable. <br>
Risk: Generated transcripts and audio are stored locally under the skill output directory. <br>
Mitigation: Apply local retention, access control, and cleanup practices appropriate for the source content. <br>
Risk: The skill requires a Gemini API key and can consume Gemini quota. <br>
Mitigation: Provide the key through environment configuration, avoid exposing it in chat logs, and monitor API quota before automation. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Files, Guidance] <br>
**Output Format:** [Markdown guidance with bash command examples; runtime output is an MP3 file path plus generated MP3 and transcript files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires GEMINI_API_KEY and ffmpeg; downloads Python packages and Chromium at runtime unless dependencies are pre-provisioned.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
