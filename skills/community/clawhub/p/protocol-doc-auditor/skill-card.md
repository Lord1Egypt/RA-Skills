## Description: <br>
Helps detect hidden attacks in API and protocol documentation by scanning integration guides for dangerous instructions like curl|bash, credential harvesting, and irrevocable identity bindings disguised as setup steps. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[andyxinweiminicloud](https://clawhub.ai/user/andyxinweiminicloud) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, engineers, and agent builders use this skill to audit API documentation, protocol specifications, and integration guides before following setup instructions. It highlights dangerous execution steps, credential exposure, data leakage, irreversible identity binding, and unnecessary privilege escalation, then recommends safer alternatives. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may quote unsafe commands from third-party documentation while explaining findings. <br>
Mitigation: Treat quoted commands as evidence to review, not as commands to execute. <br>
Risk: Pattern-based documentation review can miss novel or context-specific attack vectors. <br>
Mitigation: Use the audit report as a triage aid and perform manual expert review before following high-impact setup instructions. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/andyxinweiminicloud/protocol-doc-auditor) <br>
- [Publisher profile](https://clawhub.ai/user/andyxinweiminicloud) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown audit report with risk ratings and safer alternatives] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Rates overall document safety as SAFE, CAUTION, or DANGEROUS.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
