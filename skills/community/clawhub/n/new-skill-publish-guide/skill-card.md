## Description: <br>
Guides developers through creating a ClawHub skill package, publishing it to ClawHub, archiving release notes to IMA, and notifying a main agent. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[clawhub-master](https://clawhub.ai/user/clawhub-master) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and skill maintainers use this guide to prepare publishable ClawHub skill packages, avoid credential leakage, run ClawHub CLI release commands, and record release information in IMA. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release evidence reports apparent live IMA credentials exposed in the guide. <br>
Mitigation: Do not reuse the embedded IMA credentials; rotate or revoke them if you control the account, and replace them with your own scoped credentials stored outside the published skill. <br>
Risk: The guide includes IMA import, append, and read commands that can send or retrieve persistent external content. <br>
Mitigation: Review the target note operations and content before running any IMA command, and avoid sending sensitive or unapproved material to external persistent storage. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/clawhub-master/skills/new-skill-publish-guide) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with inline shell and JavaScript examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes release workflow checklists and examples for ClawHub CLI, IMA note operations, and main-agent notification.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release metadata and artifact frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
