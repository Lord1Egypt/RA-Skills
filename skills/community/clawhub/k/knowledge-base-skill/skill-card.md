## Description: <br>
Multi-business knowledge base with image attachment + OCR support. Manage Q&A databases by business type, auto page splitting, and intelligent search. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wwl52](https://clawhub.ai/user/wwl52) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, support teams, and operations staff use this skill to maintain local business-specific Q&A knowledge bases, search existing answers, track pending questions, attach screenshots, extract OCR text, and export Markdown documentation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Crafted business or image names can cause writes or deletes outside the intended knowledge-base directory. <br>
Mitigation: Use only simple business and image names with no slashes, absolute paths, or '..' segments, and avoid delete commands until path containment and confirmation checks are added. <br>
Risk: Screenshots and OCR text may preserve passwords, tokens, customer data, or other sensitive information in searchable local files. <br>
Mitigation: Redact sensitive screenshots before adding them and store only information that is acceptable to keep searchable on the local machine. <br>
Risk: The security verdict is suspicious, so normal installation could expose local files to unintended modification. <br>
Mitigation: Review the scripts and security guidance before installing or running the skill. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wwl52/knowledge-base-skill) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON command results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates and updates local JSON knowledge-base files, image attachments, OCR-derived text, pending-question records, statistics, and Markdown exports.] <br>

## Skill Version(s): <br>
2.1.1 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
