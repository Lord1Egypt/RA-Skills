## Description: <br>
Creates formally structured Word documents such as academic papers, research papers, white papers, technical reports, and policy briefs with TOC, equations, footnotes, endnotes, bibliography, and scholarly formatting. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[iceyliu](https://clawhub.ai/user/iceyliu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to plan and generate academic or formal .docx documents with OfficeCli, including headings, TOC, equations, footnotes or endnotes, bibliography, and QA checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill directs the agent to automatically download and run an unpinned OfficeCli installer or updater from GitHub. <br>
Mitigation: Review before installing; prefer installing a pinned, reviewed OfficeCli release yourself and prevent automatic curl/bash or PowerShell installer execution. <br>


## Reference(s): <br>
- [Creating an Academic Paper](creating.md) <br>
- [ClawHub release page](https://clawhub.ai/iceyliu/officecli-academic-paper) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands for producing a .docx file] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces a single Word .docx file through OfficeCli-driven document creation and validation steps.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
