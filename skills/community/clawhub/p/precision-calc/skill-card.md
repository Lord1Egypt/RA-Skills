## Description: <br>
Use this skill for arithmetic, finance, science, unit conversions, and everyday math calculations through Node.js and mathjs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cjhuaxin](https://clawhub.ai/user/cjhuaxin) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers can use this skill to route calculations, unit conversions, and math expression evaluation through a Node.js mathjs command. Review billing behavior before deployment because the server security evidence flags an external paid billing flow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill directs agents to use an external paid billing flow before every calculation. <br>
Mitigation: Install only when that billing behavior is intentional and user-confirmed through an approved platform mechanism. <br>
Risk: The artifact includes a hardcoded billing API key. <br>
Mitigation: Revoke the exposed key and move billing authorization to a managed secret or platform-controlled payment flow before use. <br>
Risk: Routine math requests may be routed through paid external billing even when a local calculation would be sufficient. <br>
Mitigation: Provide or require a local no-charge calculation path for ordinary math unless paid processing is explicitly requested. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/cjhuaxin/precision-calc) <br>
- [Skill homepage](https://clawhub.ai/skills/precision-calc) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Code, Guidance] <br>
**Output Format:** [Markdown with inline bash, JavaScript, and curl command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js; examples use mathjs for calculation and include an external billing API call.] <br>

## Skill Version(s): <br>
1.0.6 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
