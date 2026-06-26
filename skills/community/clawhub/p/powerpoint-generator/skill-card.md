## Description: <br>
Powerpoint Generator guides an agent through requirements research, outline planning, slide design, and post-processing to produce professional HTML presentations and editable PPTX files. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cerealaxis](https://clawhub.ai/user/cerealaxis) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, external users, developers, and presentation creators can use this skill to turn topics, requirements, source material, or outlines into structured slide decks. It is suited for roadshow decks, training materials, product introductions, and other multi-page presentation workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow may install npm or pip packages and run Python or Node.js conversion commands. <br>
Mitigation: Run it in an isolated project or container and review package installation and shell commands before execution. <br>
Risk: Slide-related data may be sent to external services when Unsplash or visual model audit features are enabled. <br>
Mitigation: Avoid confidential topics or sensitive materials when those integrations are active, or disable them for private decks. <br>
Risk: Untrusted command strings passed to the runtime logger can create execution risk. <br>
Mitigation: Do not pass untrusted strings to subagent_logger.py, and restrict logger use to reviewed commands. <br>


## Reference(s): <br>
- [Bento Grid Layout System](references/bento-grid.md) <br>
- [Core Methodology](references/method.md) <br>
- [HTML to SVG to PPTX Pipeline Compatibility Rules](references/pipeline-compat.md) <br>
- [Reusable Prompt Templates](references/prompts.md) <br>
- [Style System](references/style-system.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, files, guidance] <br>
**Output Format:** [Markdown guidance, JSON planning and style specifications, HTML slides, SVG/PNG assets, and PPTX files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes presentation artifacts under ppt-output, including preview.html, svg/*.svg, png/*.png, presentation-svg.pptx, and presentation-png.pptx.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
