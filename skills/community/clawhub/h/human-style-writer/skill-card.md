## Description: <br>
Creates long-form articles, essays, opinion pieces, and creative writing with a more human-like rhythm and style through the paid adeeptools.com service. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[qiaoshaohua](https://clawhub.ai/user/qiaoshaohua) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill to request paid long-form writing in Markdown, including articles, essays, opinion pieces, and creative prose. It creates an order, routes payment through clawtip, and then returns the generated writing after payment verification. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts and payment credentials are sent to adeeptools.com and stored in local OpenClaw order files. <br>
Mitigation: Avoid sensitive or proprietary prompts, review the charge before use, and delete old order files when they are no longer needed. <br>
Risk: The artifact includes scripts/mock_credential.py, a helper that can fake a successful payment credential. <br>
Mitigation: Do not run scripts/mock_credential.py; the publisher should remove the helper and rotate any exposed key material. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/qiaoshaohua/human-style-writer) <br>
- [Publisher profile](https://clawhub.ai/user/qiaoshaohua) <br>
- [Adeeptools homepage](https://adeeptools.com) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown article content with command-line workflow steps and status values] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a paid order and a clawtip payment credential before service execution.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
