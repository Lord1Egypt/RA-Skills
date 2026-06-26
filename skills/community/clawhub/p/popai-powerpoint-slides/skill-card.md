## Description: <br>
Creates PopAI API presentations, slide decks, and PPT content from a topic with optional PPTX, PDF, DOCX, or image reference files. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zdawang000](https://clawhub.ai/user/zdawang000) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to generate PopAI-powered slide decks from a topic, optionally using local PPTX, PDF, DOCX, or image files as references or templates. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The documented runtime command points to a hard-coded developer path rather than the installed skill directory. <br>
Mitigation: Verify or fix the command before installation so it runs the packaged `generate_ppt.py` from the installed skill directory. <br>
Risk: The skill handles a PopAI API key while calling third-party PopAI endpoints. <br>
Mitigation: Use a revocable API key with the minimum necessary access and avoid logging or sharing the key. <br>
Risk: Optional reference files are uploaded to PopAI/S3 for presentation generation. <br>
Mitigation: Upload only files that are acceptable for third-party processing and avoid confidential, regulated, or sensitive material unless that processing is approved. <br>
Risk: Generated PPTX and preview links are hosted externally. <br>
Mitigation: Treat returned download and web links as third-party hosted outputs and share them only with intended recipients. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zdawang000/popai-powerpoint-slides) <br>
- [PopAI](https://www.popai.pro) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON Lines progress events that return PPTX and web URLs.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and POPAI_API_KEY; can upload up to five local reference files; generation is expected to take 3-5 minutes.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
