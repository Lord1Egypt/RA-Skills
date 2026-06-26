## Description: <br>
Find knitting patterns. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jpengcheng523-netizen](https://clawhub.ai/user/jpengcheng523-netizen) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to find and retrieve knitting patterns for crafts, DIY workflows, and knitting-related automation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The artifact references a knitting_pattern.py helper script that is not bundled. <br>
Mitigation: Confirm the script source and review it before running any command that uses it. <br>
Risk: Pattern searches may be sent to an external service through KNITTING_API_KEY. <br>
Mitigation: Confirm the API provider, data handling expectations, and terms before sending user inputs. <br>
Risk: KNITTING_API_KEY is a secret required for use. <br>
Mitigation: Set the key through a secure environment variable or secret manager and do not commit it to source files. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jpengcheng523-netizen/jpeng-knitting-pattern) <br>
- [Publisher profile](https://clawhub.ai/user/jpengcheng523-netizen) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, shell commands, configuration, guidance] <br>
**Output Format:** [JSON results with Markdown guidance and bash commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires KNITTING_API_KEY; artifact documentation references a knitting_pattern.py script that is not bundled.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
