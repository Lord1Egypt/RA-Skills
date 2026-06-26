## Description: <br>
Organizes PDF files by using an AI provider to analyze content, extract metadata, rename files, and sort them into topic folders. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yxl184](https://clawhub.ai/user/yxl184) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and knowledge workers use this skill to configure and run a Python PDF organizer that classifies PDFs, renames them with extracted metadata, and moves them into structured folders. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: PDF text may be sent to an external AI provider during content analysis. <br>
Mitigation: Use a dedicated API key and avoid processing confidential, regulated, or proprietary documents unless the selected provider is approved for that data. <br>
Risk: The workflow can rename or move local PDF files. <br>
Mitigation: Start with dry-run mode or backed-up test PDFs before applying it to important document collections. <br>
Risk: The package evidence describes Python implementation files that were not included in the artifact. <br>
Mitigation: Review the actual implementation and dependencies before running the organizer. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/yxl184/pdf-organizer-skill) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown with inline shell commands and configuration fields] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes dry-run, incremental processing, API provider, model, folder, and character-limit configuration guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
