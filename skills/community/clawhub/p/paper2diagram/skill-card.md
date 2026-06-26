## Description: <br>
Paper2diagram analyzes research paper PDFs, extracts method and architecture details, writes an academic-review-style summary, and generates paper-style diagrams through configured Gemini and nano_banana gateways. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[qbc-oio](https://clawhub.ai/user/qbc-oio) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Researchers and technical teams use this skill to turn local research PDFs into structured method summaries and generated figures for reports, reviews, and slide preparation. It is best suited for method or architecture papers, especially in computer vision, medical imaging, and representation learning. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Selected PDFs or extracted paper content may be sent to the user's configured Gemini and Banana gateways. <br>
Mitigation: Use only trusted and approved gateways, and avoid unpublished, proprietary, or regulated papers unless those gateways are authorized for that data. <br>
Risk: The workflow depends on separate local code and configured gateway credentials that are not bundled in the skill description. <br>
Mitigation: Review the workflow repository before running it, use a virtual environment or container, and keep API keys scoped to the intended gateway use. <br>
Risk: Generated diagrams and summaries can misrepresent paper methods or results. <br>
Mitigation: Have a knowledgeable reviewer compare outputs against the source PDF before using them in reports, publications, or presentations. <br>


## Reference(s): <br>
- [Paper2diagram ClawHub listing](https://clawhub.ai/qbc-oio/paper2diagram) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and file-path outputs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce structured paper_analysis text, drawing prompts, online image links, and local image paths under outputs/.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
