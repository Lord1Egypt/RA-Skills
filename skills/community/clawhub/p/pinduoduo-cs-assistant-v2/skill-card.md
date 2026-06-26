## Description: <br>
A Pinduoduo merchant customer-service assistant that uses browser automation to log in, monitor buyer messages, match reply templates, send replies, and support after-sales workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rfdiosuao](https://clawhub.ai/user/rfdiosuao) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
E-commerce operators and support agents use this skill to assist with Pinduoduo merchant service workflows, including message triage, template-based replies, logistics questions, refunds, and after-sales follow-up. <br>

### Deployment Geography for Use: <br>
Global, subject to Pinduoduo merchant account availability and applicable customer-data requirements. <br>

## Known Risks and Mitigations: <br>
Risk: The skill automates a live merchant account and buyer conversations, with broad or under-explained safeguards for browser control, account sessions, and customer data. <br>
Mitigation: Review carefully before installing; use a dedicated Chrome profile and least-privilege merchant account, and verify where buyer conversation and order data is stored, exported, and deleted. <br>
Risk: The CDP proxy and remote browser debugging flow can expose browser-control capabilities if run without tight local controls. <br>
Mitigation: Do not run the CDP proxy unless it is locked to localhost with authentication and only available for the intended session. <br>
Risk: Automated replies can send customer-facing messages or take account actions without adequate review. <br>
Mitigation: Keep auto-reply disabled unless every send is explicitly approved and monitor replies before relying on them in production. <br>
Risk: Merchant credentials, sessions, and customer data may be exposed if stored in local configuration or export files. <br>
Mitigation: Avoid storing merchant passwords in config files, protect session and export directories, and delete retained customer data when it is no longer needed. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/rfdiosuao/pinduoduo-cs-assistant-v2) <br>
- [Pinduoduo merchant backend](https://mms.pinduoduo.com) <br>
- [Pinduoduo merchant chat](https://mms.pinduoduo.com/chat) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON configuration examples; runtime actions may send customer-service text through a merchant browser session.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js and browser access to an authenticated Pinduoduo merchant account.] <br>

## Skill Version(s): <br>
1.1.1 (source: server release metadata, SKILL.md frontmatter, package.json, skill.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
