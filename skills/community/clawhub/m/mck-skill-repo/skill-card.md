## Description: <br>
Create professional, consultant-grade PowerPoint presentations from scratch using python-pptx with McKinsey-style design. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[likaku](https://clawhub.ai/user/likaku) <br>

### License/Terms of Use: <br>
Apache-2.0 <br>


## Use Case: <br>
Employees, external users, developers, and agents use this skill to generate professional PPTX decks for pitch decks, strategy presentations, quarterly reviews, board meetings, proposals, and other business presentations. It provides layout patterns, typography, color guidance, and python-pptx examples for consistent flat-design slide generation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated scripts can write or overwrite local PPTX files. <br>
Mitigation: Use an explicit output path and review generated file-writing code before running it. <br>
Risk: The workflow may require installing Python packages with pip. <br>
Mitigation: Install in a project or virtual environment and review package installation commands before execution. <br>
Risk: Unpinned dependencies can change behavior across environments. <br>
Mitigation: For sensitive or repeatable work, pin python-pptx and lxml to reviewed versions and keep lxml patched. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/likaku/mck-skill-repo) <br>
- [Publisher profile](https://clawhub.ai/user/likaku) <br>
- [Color palette reference](references/color-palette.md) <br>
- [Layout catalog reference](references/layout-catalog.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Python code examples and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May guide agents to write local PPTX files with python-pptx and lxml cleanup.] <br>

## Skill Version(s): <br>
1.6.1 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
