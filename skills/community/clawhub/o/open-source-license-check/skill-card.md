## Description: <br>
Check if referenced bioinformatics software/code licenses allow commercial use (GPL vs MIT, etc.). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aipoch-ai](https://clawhub.ai/user/aipoch-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, engineers, and compliance reviewers use this skill to screen referenced bioinformatics tools or Python requirements for commercial-use license concerns before deeper review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: License screening can be incomplete or incorrect for copyleft, unknown, or context-dependent packages. <br>
Mitigation: Treat results as a screening aid and confirm license obligations with authoritative package metadata or legal review before commercial use. <br>
Risk: The packaged helper runs local Python code and may read a provided requirements file. <br>
Mitigation: Run it in a controlled workspace and provide only the intended software names or requirements file. <br>


## Reference(s): <br>
- [Audit Reference](references/audit-reference.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with CLI commands and structured license compatibility notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include assumptions, commercial-use warnings, compliance recommendations, and manual follow-up checks.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
