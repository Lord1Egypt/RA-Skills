## Description: <br>
Adds developer-authored annotations to the gauntlet knowledge base. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[athola](https://clawhub.ai/user/athola) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to capture module-level tribal knowledge, rationale, history, and rules as annotations for future gauntlet challenges. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Incorrect annotations can preserve misleading module rationale or rules in the gauntlet knowledge base. <br>
Mitigation: Review the target module, concept, and rationale before saving an annotation, and scan or review the skill before deployment. <br>
Risk: The skill writes YAML files under .gauntlet/annotations, which may influence future challenges. <br>
Mitigation: Confirm the generated slug and file path, inspect the YAML content, and keep changes reviewable before relying on the annotation. <br>


## Reference(s): <br>
- [Gauntlet plugin homepage](https://github.com/athola/claude-night-market/tree/master/plugins/gauntlet) <br>


## Skill Output: <br>
**Output Type(s):** [text, configuration, guidance] <br>
**Output Format:** [YAML annotation file plus concise confirmation text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes annotations under .gauntlet/annotations/<slug>.yaml when used by an agent with filesystem access.] <br>

## Skill Version(s): <br>
1.9.12 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
