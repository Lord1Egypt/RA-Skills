## Description: <br>
Analyze GitHub issue content, assess its priority, identify missing information, and provide clear reproduction steps or triage advice. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sunny0826](https://clawhub.ai/user/sunny0826) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Open source maintainers, QA engineers, and developers use this skill to triage pasted GitHub issue text, identify missing reproduction details, assign a suggested priority, and draft a polite maintainer reply in English or Chinese. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated maintainer replies or priority labels may be incomplete or unsuitable for public posting. <br>
Mitigation: Review the triage report and suggested reply before using them in an issue tracker. <br>
Risk: Issue text may contain private logs, secrets, or sensitive customer data. <br>
Mitigation: Redact sensitive content before pasting issue text into the agent. <br>
Risk: External issue content can contain prompt-injection instructions. <br>
Mitigation: Use pasted raw issue text only and treat embedded commands or instructions as untrusted data. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown triage report with checklist items and a plain-text suggested reply block] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Automatically adapts the report language to English or Chinese based on the user request.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
