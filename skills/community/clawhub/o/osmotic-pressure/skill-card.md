## Description: <br>
Detects and maps complexity imbalances across system boundaries, showing where complexity is accumulating and what may fail first. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jcools1977](https://clawhub.ai/user/jcools1977) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to inspect software boundaries, identify modules where complexity has become concentrated, and plan refactoring or architecture reviews. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Architecture findings may be incomplete or misleading when the agent sees only part of a codebase or lacks project history. <br>
Mitigation: Review the pressure analysis against repository context, ownership boundaries, tests, and recent change history before acting on recommendations. <br>
Risk: Recommended refactors can change behavior if applied without design review and tests. <br>
Mitigation: Approve proposed code changes separately, keep refactors scoped, and require normal test and review gates before merging. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jcools1977/osmotic-pressure) <br>
- [Publisher profile](https://clawhub.ai/user/jcools1977) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown or plain text architecture analysis with pressure maps, diagnoses, and recommendations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [No external API calls or executable code are required by the skill evidence.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
