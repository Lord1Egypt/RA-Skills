## Description: <br>
Automates uploading a local medical image segmentation paper to Gemini, extracting architecture analysis and diagram-generation prompts, and saving the results to a local text file. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[m1ss-cell](https://clawhub.ai/user/m1ss-cell) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, researchers, and agent users can use this skill to process locally stored medical image segmentation papers, request structured model and workflow analysis from Gemini, and collect diagram prompts for architecture figures. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The selected PDF is uploaded to Gemini using the currently signed-in Gemini account. <br>
Mitigation: Install and run only when the user is comfortable sharing the selected PDF with Gemini under that account. <br>
Risk: The skill overwrites the target output file at /home/xie/桌面/analysis/{{paper_name}}.txt. <br>
Mitigation: Use a simple paper_name value without path separators and back up or rename any existing analysis file before running. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/m1ss-cell/paper-architecture-diagram) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Structured text prompts saved to a local text file] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a paper_name parameter used to locate the input PDF and output text file.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
