## Description:

在独行录（opcmenu.com）查合作需求、主理人、产品和报名机会，并处理本人报名、私信和主办方工作台。

This skill is ready for commercial/non-commercial use.

## Publisher:

[yzlee](https://clawhub.ai/user/yzlee)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to search opcmenu collaboration needs, founders, products, services, funding, and signup opportunities. With user authorization, it supports account tasks such as signups, private messages, organizer review, profile updates, contact disclosure, attendee exports, and credit-spending actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Account actions can send messages, submit or change signups, modify profile data, disclose contact details, export attendee information, or spend credits.

Mitigation: Review prompts carefully and authorize only the specific opcmenu action, recipient, content, data export, or credit-spending step you want.

Risk: Static device keys, OAuth callbacks, passwords, or tokens could be exposed if copied into chat or tool output.

Mitigation: Use host-managed OAuth or a trusted local credential store, and do not paste, read, print, or relay secrets through the conversation.

Risk: Organizer exports and contact exchange responses can disclose personal or attendee information.

Mitigation: Generate exports or disclose contact details only for an explicit user-requested purpose, and share links or results only with the intended recipient.

Risk: Signup, organizer, profile, and workflow actions can change real opcmenu account state.

Mitigation: Preview ambiguous batch actions, preserve existing profile fields when updating, and report success only from tool receipts or confirmed returned status.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yzlee/skills/opcmenu)
- [opcmenu connection page](https://opcmenu.com/connect)
- [opcmenu public skill definition](https://opcmenu.com/agents/opcmenu.skill.md)
- [opcmenu public OpenAPI description](https://api.opcmenu.com/openapi.yaml)
- [opcmenu machine-readable navigation](https://opcmenu.com/llms.txt)
- [连接和认证](references/connection.md)
- [报名与主办方](references/signup.md)
- [合作、链位与全景工作流](references/workflows.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, API calls, Guidance]

**Output Format:** [Markdown with inline shell commands and tool/API call guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires explicit user authorization for account data, writes, contact disclosure, exports, and credit-spending actions.]

## Skill Version(s):

1.1.0 (source: ClawHub release metadata and SKILL.md metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
