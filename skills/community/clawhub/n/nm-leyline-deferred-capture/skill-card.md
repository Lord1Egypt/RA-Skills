## Description: <br>
Defines the contract for deferred-item capture across plugins. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[athola](https://clawhub.ai/user/athola) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to build or validate deferred-capture wrappers, source labels, issue templates, and compliance checks for leyline-style plugin workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Deferred-capture issue titles, context, branch or session metadata, labels, and artifact paths may expose sensitive information to repository collaborators or the public. <br>
Mitigation: Redact secrets, private customer data, internal paths, and sensitive debugging details before allowing issue creation. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/athola/skills/nm-leyline-deferred-capture) <br>
- [Leyline plugin homepage](https://github.com/athola/claude-night-market/tree/master/plugins/leyline) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration, JSON] <br>
**Output Format:** [Markdown guidance with CLI examples and JSON result shapes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Describes GitHub issue fields, labels, duplicate detection, and dry-run compliance output.] <br>

## Skill Version(s): <br>
1.9.13 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
