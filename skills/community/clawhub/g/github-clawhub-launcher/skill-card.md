## Description: <br>
Review GitHub and ClawHub release plans, metadata, tags, release notes, and final publish order before a human runs any commands. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zack-dev-cm](https://clawhub.ai/user/zack-dev-cm) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and release maintainers use this skill to review GitHub and ClawHub release metadata, public wording, release notes, test and audit status, and the human-run publish order before publishing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Release publishing, payment authority, or credentials could be delegated to the agent. <br>
Mitigation: Use the skill only as a review and wording checklist; do not provide tokens, cookies, payment authority, or permission to publish. <br>
Risk: A release could be published from an uninspected working tree or without verification. <br>
Mitigation: Have a human inspect git status, run tests, and perform GitHub or ClawHub publishing steps manually after the checklist is clean. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Markdown review with a verdict, fixes, release-note draft, checklist, and publish-order guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Does not publish releases, request credentials, or execute release commands.] <br>

## Skill Version(s): <br>
1.0.9 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
