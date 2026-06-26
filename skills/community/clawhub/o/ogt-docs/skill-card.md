## Description: <br>
Documentation-as-Source-of-Truth workflow. Use when working with projects that use docs/ as the canonical source for definitions, rules, and tasks. Routes to specialized sub-skills for specific documentation types. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[EduardoU24](https://clawhub.ai/user/EduardoU24) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to navigate and apply a docs-first workflow where project documentation defines entities, rules, and tasks before implementation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Outdated or incorrect project documentation could steer agents toward incorrect implementation decisions because this skill treats docs/ as authoritative. <br>
Mitigation: Keep docs/ reviewed and current, and require human review when documentation conflicts with observed implementation behavior. <br>
Risk: The skill references specialized ogt-docs sub-skills that are not included in this artifact. <br>
Mitigation: Review and approve each referenced sub-skill separately before relying on it in an agent workflow. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, configuration] <br>
**Output Format:** [Markdown guidance with folder structures, naming conventions, workflow references, and task routing notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [None] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
