## Description: <br>
Transcribe large audio files (100MB+, up to 1GB/12 hours) with speaker diarization using AssemblyAI API calls. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jiadong0723](https://clawhub.ai/user/jiadong0723) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and operations teams use this skill to transcribe large meeting, interview, or media audio with speaker labels and timestamps through AssemblyAI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Audio is sent to AssemblyAI for processing and may contain confidential, regulated, or privileged content. <br>
Mitigation: Use only recordings approved for third-party processing, and confirm organizational retention and privacy requirements before running the skill. <br>
Risk: The skill requires an AssemblyAI API key. <br>
Mitigation: Configure ASSEMBLYAI_API_KEY through environment variables or a secrets mechanism, and do not paste API keys into chat. <br>
Risk: Transcript outputs may be stored locally and can contain sensitive information. <br>
Mitigation: Store generated Markdown or JSON transcripts only in approved locations and apply appropriate access controls and cleanup policies. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jiadong0723/jiadong-assembly-large-audio) <br>
- [AssemblyAI upload API endpoint](https://api.assemblyai.com/v2/upload) <br>
- [AssemblyAI transcript API endpoint](https://api.assemblyai.com/v2/transcript) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown or JSON transcript content with speaker labels, timestamps, and status output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May archive transcript JSON beside the input audio file or write formatted transcript notes to a configured workspace path.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and artifact metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
