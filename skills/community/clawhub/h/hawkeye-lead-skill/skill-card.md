## Description:

招商线索池 is an operations skill that exposes ten Hawkeye merchant_lead HTTP interfaces for lead-pool review, lead details, claiming and assignment, and follow-up status, note, and acceptance-priority updates.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yiqingqiu23187](https://clawhub.ai/user/yiqingqiu23187)

### License/Terms of Use:

MIT-0

## Use Case:

Internal operations users and supporting agents use this skill to inspect private and public merchant leads, review lead statistics and details, and perform approved lead-management updates through a local CLI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can use local or shared tokens to access real lead-management data.

Mitigation: Install and run it only in a trusted internal environment, and rotate tokens that were used with an untrusted launcher or overridden domain.

Risk: Domain or cookie-name overrides can route sensitive requests outside the approved host boundary.

Mitigation: Avoid HAWKEYE_LEAD_DOMAIN and cookie-name overrides unless the target host is explicitly approved.

Risk: --plain-phone can expose plaintext phone data and may change lead state for private leads.

Mitigation: Use plaintext phone access only for a clear business need and require explicit human approval before execution.

Risk: Mutating commands can change lead ownership, follow-up status, notes, or acceptance priority.

Mitigation: Show the request body to the operator first and execute mutating commands only after explicit approval with --confirm.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yiqingqiu23187/skills/hawkeye-lead-skill)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, JSON, guidance]

**Output Format:** [Markdown guidance with CLI commands and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes command discovery, JSON Schema introspection, dry-run output with masked tokens, and structured exit-code guidance.]

## Skill Version(s):

0.1.0 (source: package.json and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
