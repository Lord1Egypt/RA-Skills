## Description: <br>
Generates fixed-size HTML presentation reports from user-provided topics or content, using built-in presentation styles, page planning, SVG/chart guidance, and quality checks for 1017 x 720 px slide-aligned output. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[panhongwei](https://clawhub.ai/user/panhongwei) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and content creators use this skill to turn supplied topics, notes, or structured material into 5-15 page HTML presentation reports with visual design systems, page layouts, cards, summaries, and charts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow can perform web lookups and load external fonts. <br>
Mitigation: Require confirmation before network access and review any external sources or font loads used in generated reports. <br>
Risk: The workflow may generate or mutate local files, including persistent style files. <br>
Mitigation: Use a dedicated output folder and prevent writes into the installed skill directory unless intentionally updating the skill. <br>
Risk: The workflow references an undeclared local Node screenshot command. <br>
Mitigation: Do not run `node screenshot_batch.js` unless the script has been reviewed or supplied by the user. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/panhongwei/html-ppt-generator) <br>
- [Skill index](artifact/skill.md) <br>
- [Canvas and structure rules](artifact/references/01-canvas.md) <br>
- [Design system and visual templates](artifact/references/02-design-system.md) <br>
- [Workflow and quality checks](artifact/references/06-workflow.md) <br>
- [Business diagram library](artifact/references/10-diagram-types.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, configuration, guidance] <br>
**Output Format:** [Markdown guidance with HTML, CSS, SVG, and shell-command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local HTML presentation pages and validation notes; screenshot/export commands may be proposed as part of the workflow.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
