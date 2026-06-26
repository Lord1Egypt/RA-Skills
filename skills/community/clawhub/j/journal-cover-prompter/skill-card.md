## Description: <br>
Use when creating journal cover images, generating scientific artwork prompts, or designing graphical abstracts. Creates detailed prompts for AI image generators to produce publication-quality scientific visuals. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aipoch-ai](https://clawhub.ai/user/aipoch-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, researchers, and content teams use this skill to create structured prompts for scientific journal cover images and graphical abstracts from a research topic, style, mood, and color palette. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Users may include confidential unpublished research details in prompts that are later sent to external image-generation tools. <br>
Mitigation: Review prompts before using external services and remove confidential or unpublished details unless the target tool and workflow are approved for that data. <br>
Risk: Documentation examples mention cover_prompter paths that are stale relative to the packaged executable path. <br>
Mitigation: Use scripts/main.py as the executable path and validate with python -m py_compile scripts/main.py and python scripts/main.py --help before relying on script execution. <br>
Risk: Broad or incomplete requests can push the skill outside its documented journal cover and graphical abstract scope. <br>
Mitigation: Require the research topic and relevant style constraints, and return missing inputs, assumptions, and next checks when the request is underspecified. <br>


## Reference(s): <br>
- [Audit Reference](references/audit-reference.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/aipoch-ai/journal-cover-prompter) <br>
- [Publisher Profile](https://clawhub.ai/user/aipoch-ai) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown and formatted text with prompt sections, technical specifications, negative prompt guidance, suggested tools, and review notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated prompts should preserve stated assumptions and stay within the journal cover and graphical abstract scope.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
