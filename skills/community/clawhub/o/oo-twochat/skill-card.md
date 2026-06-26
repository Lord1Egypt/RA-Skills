## Description: <br>
This skill lets an agent operate 2Chat through an OOMOL-connected account using the oo CLI, including listing contacts and webhooks, checking API usage, validating API keys, and creating contacts with confirmation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to let an agent perform 2Chat account operations through their connected OOMOL account, including contact lookup, webhook review, API usage checks, and contact creation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Read actions may expose contacts, webhooks, usage, and account details to the agent session. <br>
Mitigation: Install only when the agent should be allowed to operate the connected 2Chat account, and review the need for each read action before exposing account data. <br>
Risk: The contact-creation action can change 2Chat data. <br>
Mitigation: Require confirmation of the exact payload and expected effect before running write actions. <br>
Risk: Initial setup depends on the OOMOL CLI installer and account connection. <br>
Mitigation: Verify the OOMOL CLI installer and account connection before authorizing the agent to use the skill. <br>


## Reference(s): <br>
- [2Chat ClawHub listing](https://clawhub.ai/oomol/oo-twochat) <br>
- [oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [2Chat homepage](https://2chat.co) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, JSON, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON connector responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses live 2Chat connector schemas and requires confirmation before write actions.] <br>

## Skill Version(s): <br>
1.0.1 (source: evidence release and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
