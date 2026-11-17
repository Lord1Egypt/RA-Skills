## Description:

Automated search and insertion of grocery items to your active Morrisons supermarket trolley, viewing basket contents, listing delivery slots, reserving slots, managing shopping lists, and viewing previous orders.

This skill is ready for commercial/non-commercial use.

## Publisher:

[homostellaris](https://clawhub.ai/user/homostellaris)

### License/Terms of Use:

MIT-0

## Use Case:

External users with Morrisons grocery accounts use this skill to search for products, manage baskets and shopping lists, review order history, reserve delivery slots, and receive checkout reminders.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can alter a real Morrisons account by adding basket items, reserving delivery slots, deleting shopping lists, and changing list contents.

Mitigation: Manually confirm destructive or purchase-adjacent actions before asking an agent to run them.

Risk: The skill stores or uses reusable Morrisons login state and optional account credentials.

Mitigation: Protect the credential and session files, restrict filesystem access, and rotate credentials if the files are exposed.

Risk: The skill can send delivery-slot and checkout reminder details through WhatsApp.

Mitigation: Configure a Morrisons-specific WhatsApp target or disable messaging where possible.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/homostellaris/skills/morrisons)
- [Server-resolved GitHub provenance](https://github.com/homostellaris/dotfiles/tree/master/agents/skills/morrisons)
- [Bun runtime](https://bun.sh)
- [Playwright](https://playwright.dev)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, configuration]

**Output Format:** [Markdown instructions with bash commands, plus runtime text and JSON responses from the action script.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Bun, Playwright, and Morrisons authentication state or credentials.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
