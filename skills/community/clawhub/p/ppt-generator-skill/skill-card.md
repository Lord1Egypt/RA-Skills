## Description: <br>
Generates professional .pptx presentations from topics, uploaded documents, reference materials, or custom PowerPoint templates using local Python and Node tooling with the configured LLM. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yuchentsai-design](https://clawhub.ai/user/yuchentsai-design) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and presentation authors use this skill to gather requirements, analyze source documents, choose or preserve a visual style, generate a slide plan, and export a finished .pptx deck without relying on an external PPT service. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill runs local Python and Node tools, including setup and generation scripts. <br>
Mitigation: Use a virtual environment or container, review commands before execution, and avoid running check_env.py --fix against a system Python installation. <br>
Risk: Uploaded documents or decks may contain confidential content that could be sent through the configured LLM path. <br>
Mitigation: Process confidential materials only when the configured LLM path is trusted and approved for that data. <br>
Risk: Generated slide plans and decks may contain incorrect or misleading content. <br>
Mitigation: Keep validation enabled and review the slide plan and generated .pptx before sharing or using it commercially. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/yuchentsai-design/ppt-generator-skill) <br>
- [Publisher profile](https://clawhub.ai/user/yuchentsai-design) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, files, guidance] <br>
**Output Format:** [Guided prompts, markdown tables, JSON slide plans, shell commands, and generated .pptx presentation files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses local scripts for environment checks, content analysis, template analysis, chart rendering, validation, and PowerPoint generation.] <br>

## Skill Version(s): <br>
4.3.0 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
