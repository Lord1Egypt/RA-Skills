## Description: <br>
Converts PDF documents into PowerPoint presentations through the GoAI API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[goai](https://clawhub.ai/user/goai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users use this skill to convert a local PDF file or PDF URL into a PowerPoint presentation, then receive the saved PPTX path and public result URL. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Selected PDF files or PDF URLs are sent to GoAI for conversion. <br>
Mitigation: Use the skill only with documents approved for GoAI processing; avoid confidential, regulated, or internal-only content unless GoAI is approved for that data. <br>
Risk: Generated PowerPoint files are saved locally and automatically opened after successful conversion. <br>
Mitigation: Run the skill in a trusted desktop environment and inspect generated files before sharing or reusing them. <br>
Risk: The skill requires a GoAI API key and may consume account credits. <br>
Mitigation: Configure GOAI_API_KEY only in the intended agent environment and review GoAI account usage and credit behavior before running conversions. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/goai/goai-pdf-to-ppt) <br>
- [GoAI Website](https://mustgoai.com) <br>
- [GoAI PPT Service](https://ppt.mustgoai.com) <br>


## Skill Output: <br>
**Output Type(s):** [Files, Text, Shell commands, Guidance] <br>
**Output Format:** [PowerPoint .pptx file plus plain-text result path and URL lines] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires uv and GOAI_API_KEY; successful runs save a local PPTX file and return MEDIA, MEDIA_URL, RESULT_PATH, and RESULT_URL lines.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata; artifact frontmatter and pyproject list 0.3.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
