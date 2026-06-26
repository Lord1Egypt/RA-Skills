## Description: <br>
References the workspace policy playbook by listing topics, retrieving matching sections, or searching for policy keywords about tone, data use, and collaboration. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Loui1979](https://clawhub.ai/user/Loui1979) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Workspace users and agents use this skill to find and quote relevant policy sections before drafting announcements, answering governance questions, or checking rules for tone, data handling, collaboration, and change management. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The --policy-file option can point the helper at local files outside the packaged policy notebook. <br>
Mitigation: Use --policy-file only with policy documents the agent is intended to read, and verify the path before execution. <br>
Risk: The bundled policy text recommends logging sensitive actions, which could expose secrets or private details if copied literally. <br>
Mitigation: Redact sensitive values and apply normal access controls when recording security-relevant actions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Loui1979/policy-lawyer-1-0-0) <br>
- [Workspace policies](references/policies.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Plain text CLI output with Markdown policy section headings and excerpts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Lists policy topics, prints matching policy sections, or returns keyword-matched policy lines from a local Markdown policy file.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
