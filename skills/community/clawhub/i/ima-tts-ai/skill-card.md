## Description: <br>
Convert text, scripts, and captions into natural voiceovers for videos, explainers, product demos, and social posts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[allenfancy-gan](https://clawhub.ai/user/allenfancy-gan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and content creators use this skill to turn scripts, captions, and plain text into generated voiceover audio for videos, explainers, product demos, social posts, podcasts, audiobooks, accessibility workflows, and commercial narration drafts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends text prompts and an API key to IMA Studio and can create paid or credit-consuming text-to-speech jobs. <br>
Mitigation: Use only trusted IMA Studio accounts and scoped or test API keys, and avoid submitting secrets or sensitive documents for synthesis. <br>
Risk: Changing the provider endpoint could send prompts and credentials somewhere other than the documented IMA Studio API. <br>
Mitigation: Keep the default provider endpoint unless an intentional override has been reviewed. <br>
Risk: The skill stores local preference data and operation history under ~/.openclaw/. <br>
Mitigation: Delete ~/.openclaw/memory/ima_prefs.json or ~/.openclaw/logs/ima_skills/ when local preference or operation history should not be retained. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/allenfancy-gan/ima-tts-ai) <br>
- [IMA Studio homepage](https://imastudio.com) <br>
- [Volcengine TTS timbre documentation](https://www.volcengine.com/docs/6561/1257544?lang=zh) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands and optional JSON result containing task_id, URL, duration, model, and credit.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires IMA_API_KEY and returns remote audio URLs; local preferences and operation logs may be stored under ~/.openclaw/.] <br>

## Skill Version(s): <br>
1.0.8 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
