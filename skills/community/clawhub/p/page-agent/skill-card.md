## Description:

PageAgent Browser Enhancement injects PageAgent's page-controller into browser pages so agents can extract DOM state and interact with indexed elements for clicking, typing, scrolling, form filling, and page-structure reads.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dongdongbear](https://clawhub.ai/user/dongdongbear)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to inspect and operate web pages with precise DOM-based actions, especially when basic browser actions are insufficient for frontend testing or iterative design-to-code workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill injects powerful JavaScript into selected webpages and can execute page scripts.

Mitigation: Use it only on trusted target pages and avoid banking, admin, production, email, or other sensitive authenticated sites unless the browser profile is isolated.

Risk: The alternate shell wrapper accepts command arguments and the security guidance recommends avoiding it with untrusted input.

Mitigation: Prefer the documented inject-cdp.mjs path and pass only trusted target identifiers and CDP endpoints.

Risk: Unpinned local server dependencies can change behavior between installs.

Mitigation: Pin or preinstall local server dependencies instead of relying on unpinned npx resolution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dongdongbear/skills/page-agent)
- [Alibaba PageAgent](https://github.com/alibaba/page-agent)

## Skill Output:

**Output Type(s):** [text, code, shell commands, guidance]

**Output Format:** [Markdown with shell commands and JavaScript snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces DOM-state text and browser-operation snippets for targeted pages after injection.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
