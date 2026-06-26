## Description: <br>
Enables agents to operate Formsite through an OOMOL-connected account for reading, creating, updating, and deleting Formsite data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and operators use this skill to inspect Formsite forms, retrieve results, and manage webhooks through OOMOL's Formsite connector. It is suited to account-connected Formsite workflows where the agent should inspect the live action schema before running read, write, or destructive actions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires account access and sensitive credentials through an OOMOL-connected Formsite account. <br>
Mitigation: Install only when the publisher and listing are trusted, review the skill files before granting account access, and rely on OOMOL's server-side credential handling rather than exposing raw tokens. <br>
Risk: Write and destructive actions can change or remove Formsite webhook configuration. <br>
Mitigation: Inspect the live action schema, confirm the exact payload and effect with the user, and require explicit approval before running write or destructive actions. <br>


## Reference(s): <br>
- [ClawHub Formsite listing](https://clawhub.ai/oomol/oo-formsite) <br>
- [oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [Formsite homepage](https://www.formsite.com) <br>
- [OOMOL Formsite connection](https://console.oomol.com/app-connections?provider=formsite) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, API Calls, JSON, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON payloads; connector responses are JSON.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires an OOMOL-connected Formsite account and live schema inspection before action execution.] <br>

## Skill Version(s): <br>
1.0.1 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
