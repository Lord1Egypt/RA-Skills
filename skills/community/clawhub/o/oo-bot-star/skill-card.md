## Description: <br>
BotStar helps agents read, create, update, publish, and delete BotStar bots, attributes, CMS entities, CMS items, and audience user attributes through an OOMOL-connected account. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to manage BotStar bots, CMS content, bot attributes, and audience user data from an agent workflow. It supports both read-only inspection and state-changing BotStar operations when the user confirms the intended payload and effect. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Write, publish, or delete actions can alter live BotStar bots, CMS data, or user attributes. <br>
Mitigation: Review the exact payload and intended effect with the user before approving write, publish, or destructive actions. <br>
Risk: BotStar connector access is brokered through OOMOL, so account trust and connection state affect what the skill can do. <br>
Mitigation: Install only when the user trusts OOMOL to broker the BotStar connection and resolve authentication, scope, or billing issues before retrying failed actions. <br>


## Reference(s): <br>
- [BotStar homepage](https://botstar.com) <br>
- [OOMOL oo CLI](https://github.com/oomol-lab/oo-cli) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON payload examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Prompts agents to inspect live action schemas before building BotStar payloads and to require confirmation for write or destructive actions.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and skill metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
