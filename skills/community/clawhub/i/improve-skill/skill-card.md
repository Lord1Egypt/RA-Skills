## Description: <br>
This meta-skill evaluates Factory Droid skills against the current project codebase and produces prioritized, evidence-based improvement recommendations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[SoMaCoSF](https://clawhub.ai/user/SoMaCoSF) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and skill maintainers use this skill to audit how well an existing skill fits a specific codebase. It produces a structured improvement report with prioritized fixes, edge cases, and suggested skill-definition patches. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads target skill files and relevant project context broadly to assess codebase fit. <br>
Mitigation: Use explicit skill names when possible and review the generated report before acting on recommendations. <br>
Risk: Suggested SKILL.md or supporting-file edits could introduce incorrect or misleading guidance if accepted without review. <br>
Mitigation: Approve edits only after checking the proposed changes against the target skill's purpose and project behavior. <br>


## Reference(s): <br>
- [ClawHub skill release page](https://clawhub.ai/SoMaCoSF/improve-skill) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, guidance] <br>
**Output Format:** [Markdown report with prioritized findings and suggested SKILL.md patches] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose edits to SKILL.md and supporting files after user approval.] <br>

## Skill Version(s): <br>
0.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
