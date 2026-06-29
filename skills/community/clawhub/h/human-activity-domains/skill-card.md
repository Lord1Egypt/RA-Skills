## Description: <br>
Human Activity Domains provides a 6 by 6 taxonomy and reference index for classifying human activity domains across 36 major domains and 108 subdomains. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wangjiaocheng](https://clawhub.ai/user/wangjiaocheng) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents and developers use this skill to classify user requests into human activity domains, load the relevant domain reference material, and produce domain positioning reports, skill references, collaboration reports, or solution guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill is broad enough to steer an agent into sensitive operational workflows, including financial, medical, HR, security-testing, database, legal, and destructive-data contexts. <br>
Mitigation: Use the skill primarily for classification and read-only reference lookup unless the user explicitly approves a sensitive workflow and qualified review is available. <br>
Risk: Domain reference material may produce workflow guidance that exceeds simple taxonomy lookup. <br>
Mitigation: Review generated guidance before action, especially where outputs could affect regulated, safety-critical, or destructive operations. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wangjiaocheng/skills/human-activity-domains) <br>
- [Publisher profile](https://clawhub.ai/user/wangjiaocheng) <br>
- [Skill definition and 108-domain index](artifact/SKILL.md) <br>
- [Distributed domain reference materials](artifact/references/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown or structured text reports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May reference domain-specific skill files, catalogs, requirements, and exemplar material when a task maps to one or more activity domains.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
