## Description: <br>
Convert structured single-slide or small deck HTML files into editable PPTX slides with native text boxes, shapes, chips, arrows, and panels. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[textboy](https://clawhub.ai/user/textboy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and presentation-focused agents use this skill to convert supported fixed-layout HTML slide designs into editable PowerPoint files, especially architecture, analyst-style, and AI runtime pages. When a design does not match an existing slide family, the skill guides the agent to add a preset before conversion. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill runs local Node.js scripts and reads or writes files as part of HTML-to-PowerPoint conversion. <br>
Mitigation: Install dependencies with the included lockfile where possible, run the environment check before use, and keep inputs and outputs in intended project directories. <br>
Risk: Unsupported HTML families can produce structurally incorrect slide output if forced through an existing preset. <br>
Mitigation: Identify the page family first and add a new preset with extraction, layout, and QA rules when the HTML does not match supported presets. <br>
Risk: Generated slides can still have spacing, overflow, clipping, or arrow-direction issues. <br>
Mitigation: Run the bundled preflight QA and visually inspect the PowerPoint output before relying on it. <br>
Risk: Agent-added presets may introduce incorrect mapping logic or misleading presentation structure. <br>
Mitigation: Review proposed preset edits before use and keep the semantic extraction, rendering, and QA rules aligned with the target slide family. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/textboy/present-ppt) <br>
- [README](README.md) <br>
- [Setup and portability](references/setup.md) <br>
- [Usage Principles](references/usage-principles.md) <br>
- [Preset decision rules](references/preset-decision-rules.md) <br>
- [Preset guide](references/presets.md) <br>
- [New preset template checklist](references/preset-template.md) <br>
- [QA heuristics](references/qa-heuristics.md) <br>
- [Roadmap](references/roadmap.md) <br>
- [Upstream html-slide-to-pptx reference](https://github.com/mucsbr/ppt-agent-workflow-san/tree/main/html-slide-to-pptx) <br>
- [mk-present project](https://github.com/textboy/mk-present) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, files] <br>
**Output Format:** [Markdown guidance with shell commands and generated PPTX, JSON model, or QA report files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs are local files, commonly .pptx decks plus optional JSON model and QA report artifacts.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
