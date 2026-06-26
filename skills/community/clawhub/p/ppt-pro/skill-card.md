## Description: <br>
PPT Pro guides an agent through a full presentation workflow, from requirements research and outline planning to HTML slide generation and optional editable PPTX conversion. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[in12hacker](https://clawhub.ai/user/in12hacker) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and presentation authors use this skill to turn a topic, source material, or outline into structured slide plans, HTML presentation pages, preview files, and PPTX outputs. It is intended for report decks, training materials, product introductions, roadshow decks, and other presentation workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can run local Python and Node.js scripts, install pip or npm packages, and use browser rendering. <br>
Mitigation: Run it in a disposable or project-scoped workspace and review commands before execution. <br>
Risk: Generated planning and HTML content could carry incorrect, misleading, or untrusted presentation material. <br>
Mitigation: Review generated planning JSON and avoid feeding untrusted HTML into the conversion pipeline. <br>
Risk: The WPS helper may make persistent WPS configuration changes. <br>
Mitigation: Use the WPS helper only when those local configuration changes are acceptable. <br>
Risk: Some helper paths may read files outside the intended reference folder. <br>
Mitigation: Run the skill with only the project files needed for the presentation and inspect outputs before reuse. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/in12hacker/ppt-pro) <br>
- [PPTX editable pipeline rules](references/pptx-pipeline.md) <br>
- [Execution rules](references/execution-rules.md) <br>
- [Quality checks](references/quality-checks.md) <br>
- [Planning schema](references/planning.schema.json) <br>
- [Resource registry](references/resource-registry.md) <br>
- [Image generation guidance](references/image-generation.md) <br>
- [WPS testing notes](WPS_TESTING.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files] <br>
**Output Format:** [Markdown guidance, JSON planning data, HTML slide files, preview HTML, PNG assets, and PPTX files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May use Python, Node.js, browser rendering, local package installation, and optional WPS-based validation depending on available tools and selected pipeline.] <br>

## Skill Version(s): <br>
9.7.0 (source: release evidence and SKILL.md metadata; pyproject.toml reports 9.6.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
