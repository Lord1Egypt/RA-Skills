## Description: <br>
Analyze videos with Google Gemini API for summaries, Q&A, timestamped transcription, scene and timeline detection, clipping, FPS control, multi-video comparison, and YouTube URL analysis. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lnj22](https://clawhub.ai/user/lnj22) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and video-analysis practitioners use this skill to guide Gemini API workflows that summarize videos, answer timestamped questions, produce transcripts, detect scenes, compare videos, and analyze public YouTube URLs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Using the skill may send selected videos, prompts, clips, or YouTube URLs to Google Gemini and requires handling a Gemini API key. <br>
Mitigation: Use only authorized media, protect GEMINI_API_KEY, and review Google privacy, retention, and billing terms before use. <br>
Risk: Generated summaries, transcripts, timestamps, or event timelines may be incomplete or inaccurate for long, clipped, low-FPS, or visually dense videos. <br>
Mitigation: Review outputs against the source media, request strict MM:SS formatting, chunk long videos when needed, and validate important events before relying on them. <br>


## Reference(s): <br>
- [Gemini Video API Docs](https://ai.google.dev/gemini-api/docs/video-understanding) <br>
- [Google AI Studio API Key](https://aistudio.google.com/apikey) <br>
- [Gemini API Pricing](https://ai.google.dev/pricing) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Code, Configuration, JSON] <br>
**Output Format:** [Markdown guidance with Python code examples and a JSON output schema] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a Gemini API key and may process user-selected video files, clips, prompts, or public YouTube URLs through Google Gemini.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
