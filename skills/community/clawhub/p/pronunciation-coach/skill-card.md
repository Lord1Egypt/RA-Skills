## Description: <br>
Pronunciation coaching with real voice analysis using Azure Speech Services. Analyzes audio files for phoneme-level accuracy, fluency, prosody, and intonation scores. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Crazybuffon](https://clawhub.ai/user/Crazybuffon) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and agent operators use this skill to assess spoken English recordings against reference text, generate pronunciation scores, and produce coaching feedback for problem words, phonemes, fluency, prosody, and practice steps. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Selected local voice recordings and reference text are sent to Microsoft Azure Speech Services for pronunciation assessment. <br>
Mitigation: Install only when that data flow is acceptable, verify the selected audio file before running the assessment, and disclose the Azure processing path to users. <br>
Risk: Azure Speech credentials are required to run the assessment. <br>
Mitigation: Use a restricted Azure Speech key and provide credentials through AZURE_SPEECH_KEY and AZURE_SPEECH_REGION environment variables. <br>
Risk: The skill depends on local audio conversion and report-generation tooling. <br>
Mitigation: Ensure ffmpeg and Node.js are installed before use and review command output for conversion or recognition failures. <br>


## Reference(s): <br>
- [Common Phoneme Issues & Coaching Tips](references/phoneme-guide.md) <br>
- [Pronunciation Coach on ClawHub](https://clawhub.ai/Crazybuffon/pronunciation-coach) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands, Guidance] <br>
**Output Format:** [Plain text or Markdown coaching report, with raw Azure Speech JSON available from the assessment script] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a local audio file, reference text, Azure Speech credentials in environment variables, ffmpeg, and Node.js.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release metadata and skill.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
