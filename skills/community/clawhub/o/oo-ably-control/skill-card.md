## Description: <br>
Ably Control helps agents manage Ably apps, API keys, queues, account details, and statistics through the OOMOL oo CLI connector. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to inspect and manage Ably Control resources in an OOMOL-connected account, including app, key, queue, account, and statistics workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: High-impact Ably account changes can create, update, revoke, or delete apps, queues, and API keys. <br>
Mitigation: Require explicit user confirmation for app deletion, queue deletion, key creation, key updates, and key revocation before execution. <br>
Risk: The get_current_account action may expose Ably Control token output. <br>
Mitigation: Avoid running get_current_account unless token fields are redacted before display or storage. <br>
Risk: Using this skill gives an agent operational access through the connected Ably account. <br>
Mitigation: Install and use it only when the user trusts OOMOL and the connected Ably account has appropriate permissions for the task. <br>


## Reference(s): <br>
- [Ably Control homepage](https://ably.com) <br>
- [OOMOL oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [ClawHub skill page](https://clawhub.ai/oomol/skills/oo-ably-control) <br>
- [OOMOL publisher profile](https://clawhub.ai/user/oomol) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON payloads.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May run OOMOL oo CLI actions that return JSON response data and execution metadata.] <br>

## Skill Version(s): <br>
1.0.0 (source: SKILL.md frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
