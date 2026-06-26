## Description: <br>
Create, inspect, and edit Microsoft PowerPoint presentations and PPTX decks with reliable layouts, templates, placeholders, notes, charts, and visual QA. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ivangdavila](https://clawhub.ai/user/ivangdavila) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill when working with Microsoft PowerPoint decks that need reliable text extraction, template-aware editing, chart and placeholder handling, notes or comments review, and final visual QA. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: PowerPoint decks can contain non-visible information such as speaker notes, comments, linked assets, and template leftovers. <br>
Mitigation: Use the skill only with decks the agent is allowed to inspect or modify, and include notes, comments, labels, legends, and linked media in review. <br>
Risk: Template or placeholder assumptions can place content in the wrong box, layer, layout, or chart structure. <br>
Mitigation: Inventory layouts, placeholders, masters, charts, notes, comments, and media before editing, then verify affected slides after each change. <br>
Risk: A deck can pass text inspection while still having visual issues such as overflow, clipping, weak contrast, or alignment problems. <br>
Mitigation: Run content QA and rendered visual QA separately, including at least one fix-and-verify pass for layout-sensitive decks. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ivangdavila/powerpoint-pptx) <br>
- [Publisher profile](https://clawhub.ai/user/ivangdavila) <br>
- [Skill homepage](https://clawic.com/skills/powerpoint-pptx) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Markdown, Code, Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown, code snippets, shell commands, and deck-editing guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce or modify PPTX files when the host agent has suitable file tools.] <br>

## Skill Version(s): <br>
1.0.1 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
