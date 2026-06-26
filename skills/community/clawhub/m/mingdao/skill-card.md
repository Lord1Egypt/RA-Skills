## Description: <br>
Mingdao is a low-code APaaS assistant for application building, worksheet design, workflow automation, data management, permissions, custom pages, and open API integration. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhangifonly](https://clawhub.ai/user/zhangifonly) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, builders, and operations teams use this skill to design Mingdao low-code applications for CRM, project management, approvals, inventory, and HR workflows. It provides guidance, examples, and code snippets for worksheets, workflows, permissions, custom pages, and API integrations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Mingdao API credentials or signs could be exposed when adapting API examples. <br>
Mitigation: Use least-privilege credentials, keep secrets out of prompts and shared outputs, and store credentials only in approved secret-management systems. <br>
Risk: Record update or delete examples could affect production data if copied directly. <br>
Mitigation: Test update and delete calls outside production first, require review for destructive actions, and verify worksheet and row identifiers before execution. <br>
Risk: Workflow and API examples may process personal identity data. <br>
Mitigation: Send personal data only to vetted services with proper authorization, minimize the data shared, and follow applicable privacy controls. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/zhangifonly/mingdao) <br>
- [Skill source](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Configuration] <br>
**Output Format:** [Markdown with tables and inline JavaScript and Python code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include Mingdao workflow patterns, worksheet configuration guidance, API examples, and permission design recommendations.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
