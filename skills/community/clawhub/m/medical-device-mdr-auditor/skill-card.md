## Description: <br>
Audits medical device technical files against EU MDR 2017/745 regulations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aipoch-ai](https://clawhub.ai/user/aipoch-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Regulatory, quality, and engineering users can use this skill to check medical device technical-file folders or batch configurations for expected EU MDR documents and receive a structured compliance report. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads local technical-file folders and can write reports that may include confidential paths or filenames. <br>
Mitigation: Run it only on the intended technical-file folder, write output to a controlled path, and review reports before sharing. <br>
Risk: Dependencies are listed without pinned versions. <br>
Mitigation: Review and pin dependencies before installing in managed or production environments. <br>
Risk: Audit results are a helper output and may not cover every regulatory or device-specific obligation. <br>
Mitigation: Use reports as review support and validate final MDR conclusions with qualified regulatory reviewers. <br>


## Reference(s): <br>
- [Audit Reference](references/audit-reference.md) <br>
- [ClawHub skill page](https://clawhub.ai/aipoch-ai/medical-device-mdr-auditor) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance and JSON compliance reports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports may include audit date, device class, input path, compliance status, findings, summary counts, and exit status.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and target metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
