## Description: <br>
Monitor Nate B Jones's YouTube channel, pull each new video transcript (YouTube captions or auto-transcribed audio), summarize it with an abstract + bullet highlights + reference links, and distribute the digest via email, chat, and/or a document per user-configured outputs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[arpee](https://clawhub.ai/user/arpee) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Subscribers, researchers, and operators use this skill to monitor Nate B Jones uploads, summarize each new video, and send a concise digest to configured email, chat, or document destinations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated summaries may be sent outside the local environment through configured email, chat, or document destinations. <br>
Mitigation: Before running, confirm recipients, chat targets, document sharing settings, and whether scheduled automation should be enabled. <br>
Risk: The workflow relies on YouTube, transcript, email, chat, and document credentials that may grant access beyond this single digest task. <br>
Mitigation: Use the narrowest practical credential scopes and review configured API keys and service permissions before deployment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/arpee/nate-b-jones-digest) <br>
- [Configuration example](references/config-example.yml) <br>
- [Nate B Jones YouTube channel](https://www.youtube.com/@NateBJones) <br>
- [youtube-transcript-api](https://pypi.org/project/youtube-transcript-api/) <br>
- [Whisper CLI](https://github.com/openai/whisper) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown digest with optional plain text or HTML delivery outputs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Digests include an abstract, bullet highlights, and reference links; delivery channels and transcript handling are controlled by user configuration.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
