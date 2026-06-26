## Description: <br>
Extracts English vocabulary from a PDF and generates an MP3 that reads each word or phrase twice. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[effeceee](https://clawhub.ai/user/effeceee) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Learners, teachers, and agents preparing English study materials can turn a PDF vocabulary list into a British English MP3 for listening practice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads the selected PDF and uses edge-tts to synthesize extracted vocabulary text. <br>
Mitigation: Use an explicit PDF path when possible and avoid sensitive PDFs unless the edge-tts data flow is acceptable. <br>
Risk: Full lines beginning with English may be included in the spoken output. <br>
Mitigation: Review the source PDF formatting and the generated word list before relying on the MP3. <br>
Risk: The skill invokes local edge-tts and ffmpeg binaries and writes the resulting MP3 under /tmp. <br>
Mitigation: Install trusted dependencies and inspect the generated file before sharing it. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/effeceee/pdf-vocab-audio) <br>


## Skill Output: <br>
**Output Type(s):** [Audio, Files, Text] <br>
**Output Format:** [MP3 audio file plus console status text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Each extracted English word or phrase is spoken twice with one-second pauses; output is saved under /tmp.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
