## Description: <br>
Splits a user-provided PDF into Markdown text, extracted figure PNGs, and a manifest so an agent can analyze the text first and open figures only when requested. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xjhveteran199-bit](https://clawhub.ai/user/xjhveteran199-bit) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers, researchers, and analysts use this skill when they need an agent to process uploaded PDFs, especially papers, into readable Markdown while keeping figures available as local files for targeted review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow may install Python packages and create local output folders while processing user-provided PDFs. <br>
Mitigation: Use a project or virtual environment for sensitive work and confirm the PDF input path and output directory before running commands. <br>
Risk: Converted Markdown can lose layout hierarchy, equations, and data embedded inside figures. <br>
Mitigation: Use the original PDF or extracted figure files to verify formulas, visual data, and layout-sensitive claims. <br>
Risk: Caption-based figure classification can place unusual or small legitimate figures in the miscellaneous folder. <br>
Mitigation: Check the manifest and miscellaneous folder when expected figures are missing, and adjust extraction thresholds when needed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/xjhveteran199-bit/skills/pdf-extract-md-figs) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Files, Shell commands, Guidance] <br>
**Output Format:** [Markdown instructions with bash commands; generated artifacts include Markdown text, PNG figure files, and a text manifest.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates local output folders and opens figure images only on explicit request.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
