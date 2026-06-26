## Description: <br>
Helps users navigate a multi-branch A-to-K business process, plan paths, query node skill codes, and view branch structure. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[JopYin](https://clawhub.ai/user/JopYin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Operations teams, process owners, and agents use this skill to determine next steps in an A-to-K business workflow, identify routes to endpoints, and retrieve check, execution, and judgment codes for process nodes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The optional CLI helper can execute unintended local Python code if a crafted node name is passed. <br>
Mitigation: Use only known node IDs with scripts/navigate.sh, review the helper before installation, or patch it to pass node values as Python arguments rather than embedding them in Python source. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/JopYin/process-flow-navigator) <br>
- [README](README.md) <br>
- [Flow Rules Data](data/flow-rules.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown responses with optional shell command examples and CLI text output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May reference local flow rules and node IDs; the shell helper expects known node names.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and README changelog) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
