## Description: <br>
Search articles on any topic, generate a two-host dialogue script, and synthesize podcast audio via TTS. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[besty0121](https://clawhub.ai/user/besty0121) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and content creators use this skill to turn source articles or topic searches into a concise two-speaker podcast script and synthesized MP3 audio. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill performs outbound article fetching and podcast synthesis workflows. <br>
Mitigation: Use trusted source URLs, avoid private or regulated content, and set explicit source and duration limits for accuracy-sensitive topics. <br>
Risk: Podcast script text is sent to the Edge TTS provider during audio synthesis. <br>
Mitigation: Do not include confidential, personal, or regulated text in scripts unless the deployment has approved that data flow. <br>
Risk: The Python TTS dependency is documented without a pinned version. <br>
Mitigation: Pin and review the dependency version in controlled deployments before use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/besty0121/podcast-agent) <br>
- [Publisher profile](https://clawhub.ai/user/besty0121) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Files, Guidance] <br>
**Output Format:** [Markdown guidance, JSON dialogue scripts, shell commands, and MP3 audio files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generates audio files under the skill output directory; requires Python and edge-tts, with ffmpeg improving audio concatenation quality when available.] <br>

## Skill Version(s): <br>
1.0.2 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
