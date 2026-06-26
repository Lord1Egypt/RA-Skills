## Description: <br>
Reads and analyzes MockPlus online design pages, extracting project information, page structure, component details, interactions, and comments from MockPlus links. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[A-din](https://clawhub.ai/user/A-din) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, designers, and agent users use this skill to inspect MockPlus prototypes and summarize design structure, interaction flows, project details, and implementation-relevant notes in a standardized Markdown format. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill includes hardcoded local project paths and npm install/run commands that do not fit a read-only MockPlus analysis workflow. <br>
Mitigation: Review the skill before installing or executing it, and remove or inspect local path references and npm commands unless the user explicitly wants that app workflow. <br>
Risk: MockPlus pages may require login or project permissions, so extracted design information may be incomplete. <br>
Mitigation: Use authenticated, authorized MockPlus access and clearly note missing or inaccessible pages in the analysis output. <br>


## Reference(s): <br>
- [ClawHub Mockplus Reader release](https://clawhub.ai/A-din/mockplus-reader) <br>
- [MockPlus](https://www.mockplus.com/) <br>
- [MockPlus RP](https://rp.mockplus.com/) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown with structured sections and inline shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include project information, page structure, interaction notes, comments, access limitations, and implementation guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
