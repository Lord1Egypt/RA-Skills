## Description: <br>
Generates MediTrust meeting minutes by transcribing meeting audio with Fun-ASR, standardizing healthcare and insurance terminology, attributing speakers, and producing structured minutes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jiadong0723](https://clawhub.ai/user/jiadong0723) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees and operations teams use this skill to turn Chinese business meeting recordings into structured meeting minutes, raw transcripts, standardized terminology, speaker attributions, consensus items, and action items. It is tailored to MediTrust healthcare and insurance meeting workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill embeds a default cloud API key. <br>
Mitigation: Remove the embedded key, rotate it if it was real or exposed, and require users to provide DASHSCOPE_API_KEY through a secure environment variable. <br>
Risk: Meeting audio, transcripts, and minutes may contain confidential, regulated, or internal information. <br>
Mitigation: Use only when external DashScope processing and public or CDN-hosted audio URLs are approved for the data, and define retention and deletion rules for raw transcripts and generated minutes. <br>
Risk: Speaker attribution and terminology normalization can be wrong or overconfident. <br>
Mitigation: Require human review of speaker names, action items, deadlines, and terminology before relying on or distributing the minutes. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jiadong0723/jiadong-meixin-meeting) <br>
- [Publisher profile](https://clawhub.ai/user/jiadong0723) <br>
- [DashScope Fun-ASR transcription endpoint](https://dashscope.aliyuncs.com/api/v1/services/audio/asr/transcription) <br>
- [DashScope task status endpoint](https://dashscope.aliyuncs.com/api/v1/tasks/{task_id}) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown meeting minutes, raw transcript text, and console status output.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a meeting audio file, a publicly accessible audio URL, and DASHSCOPE_API_KEY; writes meeting artifacts under /workspace/memory/meetings/.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence and artifact metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
