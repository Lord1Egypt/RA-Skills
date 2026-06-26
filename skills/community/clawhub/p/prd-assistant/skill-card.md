## Description: <br>
PRD-Writer helps agents draft, refine, and structure product requirements documents using a three-stage workflow, MoSCoW prioritization, Mermaid diagrams, and optional review sections. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xx235300](https://clawhub.ai/user/xx235300) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Product managers, founders, and product teams use this skill to turn initial ideas, rough requirements, or existing drafts into structured PRDs with acceptance criteria, priorities, diagrams, and review prompts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated HTML chart attachments load Mermaid JavaScript from jsDelivr when opened. <br>
Mitigation: Review generated HTML before opening or sharing it, and avoid using the attachment workflow in sensitive or offline environments unless the dependency is approved. <br>
Risk: Broad PRD and requirements-document triggers may activate this workflow for generic product-documentation prompts. <br>
Mitigation: Confirm that PRD generation is intended before following the workflow, especially when the user only asks for general requirements guidance. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/xx235300/prd-assistant) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/xx235300) <br>
- [Source provenance unavailable](unavailable) <br>
- [README](artifact/README.md) <br>
- [Skill definition](artifact/SKILL.md) <br>
- [English PRD template](artifact/PRD模板_英文.md) <br>
- [Chinese PRD template](artifact/PRD模板_中文.md) <br>
- [Mermaid HTML template](artifact/HTML模板/mermaid_template.html) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, files, guidance] <br>
**Output Format:** [Markdown PRD sections with Mermaid diagram code and optional HTML attachment content] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports complete, standard, and quick PRD modes; standard and complete modes can include review sections.] <br>

## Skill Version(s): <br>
3.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
