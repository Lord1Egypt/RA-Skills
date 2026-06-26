## Description: <br>
Create animation-rich, zero-dependency HTML presentations from scratch or by converting PowerPoint files into browser-ready slide decks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[LeoYeAI](https://clawhub.ai/user/LeoYeAI) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers, presenters, and OpenClaw users use this skill to create new HTML slide decks, convert PowerPoint files to web slides, or enhance existing HTML presentations with curated visual styles and navigation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: PPT conversion and image processing read local files and may extract assets into an output folder. <br>
Mitigation: Point the agent only at the specific presentation, HTML file, or asset folder intended for the task and review extracted files before sharing. <br>
Risk: Optional Python packages are needed for PPT conversion and image processing. <br>
Mitigation: Install python-pptx or Pillow only when those features are required and use the local environment approved for the project. <br>
Risk: Inline editing can persist slide text in browser localStorage on shared browsers. <br>
Mitigation: Avoid inline editing on shared browsers or clear the site's localStorage after editing. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/LeoYeAI/myclaw-frontend-slides) <br>
- [Publisher profile](https://clawhub.ai/user/LeoYeAI) <br>
- [Style Presets Reference](references/STYLE_PRESETS.md) <br>
- [OpenClaw](https://github.com/openclaw/openclaw) <br>
- [MyClaw.ai](https://myclaw.ai) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files] <br>
**Output Format:** [Markdown guidance with HTML, CSS, JavaScript, Python, and shell command snippets; generated agent work may include single-file HTML presentations and style preview files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May use optional local Python packages for PPT conversion or image processing and may create temporary style preview files.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
