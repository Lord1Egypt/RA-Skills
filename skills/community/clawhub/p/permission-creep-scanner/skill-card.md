## Description: <br>
Helps detect permission creep in AI agent skills by flagging when a skill's actual code accesses resources far beyond what its declared purpose requires. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[andyxinweiminicloud](https://clawhub.ai/user/andyxinweiminicloud) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and security reviewers use this skill to inspect AI agent skills for over-broad file, environment, network, subprocess, and system access relative to the skill's stated purpose. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Inputs being analyzed may contain untrusted code or URLs. <br>
Mitigation: Review them as data only and avoid executing analyzed snippets or following analyzed URLs during the audit. <br>
Risk: The skill documentation includes an illustrative malicious example. <br>
Mitigation: Use the example only to understand expected findings; do not run the sample code or command shown there. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/andyxinweiminicloud/permission-creep-scanner) <br>
- [Skill Source Artifact](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Structured permission audit in Markdown or plain text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes declared scope, access inventory, mismatch flags, risk rating, and recommendation.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
