## Description: <br>
Motor Drawing Review helps agents review motor engineering drawings for pole-slot matching, dimension annotations, technical requirements, tolerance fits, and drawing review reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yongjie666888](https://clawhub.ai/user/yongjie666888) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Motor and electrical engineers use this skill to structure reviews of motor engineering drawings, generate checklist-style review materials, and draft standardized issue reports for dimensions, tolerances, GD&T, and technical requirements. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill is a checklist and reference aid, not certified engineering validation or proof that a motor drawing is correct. <br>
Mitigation: Use it to organize review work, then have a qualified engineer verify safety-critical designs and final drawing decisions. <br>
Risk: The structural checklist command currently has a non-security runtime bug. <br>
Mitigation: Use the full or electromagnetic checklist paths, or fix and test the structural checklist script before relying on that command. <br>


## Reference(s): <br>
- [Motor Drawing GD&T Reference](references/gdt-reference.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/yongjie666888/motor-drawing-review) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown reports, plain-text checklists, and command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Checklist output can be printed or written to a text file; engineering conclusions require qualified human review.] <br>

## Skill Version(s): <br>
1.2.0 (source: SKILL.md frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
