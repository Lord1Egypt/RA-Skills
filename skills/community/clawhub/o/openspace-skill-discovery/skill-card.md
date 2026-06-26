## Description: <br>
Searches for reusable skills across OpenSpace's local registry and cloud community so agents can discover relevant capabilities before handling a task. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[x-rayluan](https://clawhub.ai/user/x-rayluan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents and developers use this skill to search local and cloud OpenSpace skill registries, compare relevant matches, and decide whether to follow or delegate to a discovered skill. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Auto-importing community skills during search may bring unreviewed instructions into the local environment. <br>
Mitigation: Prefer setting auto_import to false and review any imported SKILL.md before allowing the agent to follow it. <br>
Risk: A discovered skill may lead the agent toward misleading or unsafe guidance if followed without review. <br>
Mitigation: Tell the user what was found, recommend next steps, and scan or review skills before deployment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/x-rayluan/openspace-skill-discovery) <br>
- [Packaged skill instructions](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, guidance] <br>
**Output Format:** [Markdown or structured text search results with recommendations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include local paths for auto-imported cloud skills; results are not executed.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
