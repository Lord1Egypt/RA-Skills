## Description: <br>
Group Director creates short videos from Claw-prepared prompts for Feishu or Lark group-chat scenarios, then returns a plain video URL or failure text. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Hei-MaoM](https://clawhub.ai/user/Hei-MaoM) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents using Claw in Feishu or Lark group chats use this skill after Claw has already prepared the final video prompt. The skill creates a SenseAudio video task, polls for completion, and returns a plain video URL or plain-text failure message. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Final video prompts are sent to SenseAudio for generation. <br>
Mitigation: Install only when SenseAudio processing is acceptable and avoid including sensitive group-chat details in prompts. <br>
Risk: The skill requires a SenseAudio API key and supports an overrideable provider base URL. <br>
Mitigation: Use a dedicated SENSEAUDIO_API_KEY where possible and keep SENSEAUDIO_BASE_URL fixed to the intended provider endpoint. <br>
Risk: Provider errors or raw responses could expose unnecessary operational details if pasted into Feishu or Lark. <br>
Mitigation: Return only plain natural-language status, failure text, or the final video URL, and do not paste raw error output into chat. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/Hei-MaoM/group-director) <br>
- [Claw Integration Notes](references/integration_cn.md) <br>
- [Provider Notes](references/provider_notes.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Plain text and Markdown with inline bash examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Create returns a task_id; polling returns a video URL, status, failure, or timeout message. Feishu/Lark delivery should not include raw JSON or provider payloads.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
