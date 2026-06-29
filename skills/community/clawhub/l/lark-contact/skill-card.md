## Description: <br>
Looks up Lark/Feishu contacts by name, email, or open_id so an agent can resolve people before messaging, scheduling, or presenting directory details. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gu2003li](https://clawhub.ai/user/gu2003li) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees and agents working in a configured Lark tenant use this skill to resolve names or emails to open_id values and to retrieve directory details such as name, department, email, and contact fields. It is intended for lookup before downstream actions such as sending messages, inviting people, or scheduling meetings. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill returns workplace directory data such as names, emails, departments, chat IDs, and contact details. <br>
Mitigation: Install it only where lark-cli is configured for the intended tenant and users are allowed to look up colleague contact details. <br>
Risk: Ambiguous name or email matches could lead an agent to use the wrong person in a downstream message, group invite, or meeting request. <br>
Mitigation: Confirm ambiguous candidates with the user before using an ID for an action with side effects. <br>
Risk: Lookup results are constrained by tenant permissions and visibility rules, so some profile fields may be unavailable or empty. <br>
Mitigation: Treat empty fields as visibility-limited data and guide users to tenant administration or the returned console URL when permission errors occur. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/gu2003li/lark-contact) <br>
- [+get-user reference](artifact/references/lark-contact-get-user.md) <br>
- [+search-user reference](artifact/references/lark-contact-search-user.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline shell commands and JSON-oriented CLI output guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires an existing lark-cli configuration for the intended Lark tenant.] <br>

## Skill Version(s): <br>
1.0.0 (source: SKILL.md frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
