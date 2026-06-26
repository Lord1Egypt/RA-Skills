## Description: <br>
Generates PowerPoint presentations from a topic prompt by using Gemini to plan each slide and create full-bleed slide images. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jinpeng](https://clawhub.ai/user/jinpeng) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and presentation creators use this skill to generate visual PowerPoint decks from a topic prompt, with Gemini producing the slide outline and image-based slide designs. It is suited for drafts at 1K resolution and final decks at 2K or 4K when higher image quality is needed. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Gemini API keys are sensitive credentials. <br>
Mitigation: Provide the key through a trusted environment variable or secure runtime secret, and avoid exposing it in shared chat transcripts, logs, or checked-in files. <br>
Risk: Presentation prompts and generated content are sent to Gemini or to the configured custom API endpoint. <br>
Mitigation: Use only trusted Gemini endpoints and avoid confidential or regulated content unless that endpoint is approved for the data. <br>
Risk: The script creates a local output directory containing intermediate slide plans, image prompts, request logs, PNG images, and the final PPTX. <br>
Mitigation: Review the output folder before sharing, and remove intermediate files when they are no longer needed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jinpeng/nano-banana-pro-pptx) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration instructions, Files, Guidance] <br>
**Output Format:** [Markdown guidance with a bash command; local PPTX, PNG, JSON, and log files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a Gemini API key, accepts an optional custom Gemini base URL, supports 1-50 slides, and creates a local output directory.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
