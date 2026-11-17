## Description:

Search and buy digital game codes, eShop cards, PSN vouchers, Roblox, and related products from Play-Asia.com through HTTP or MCP.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tom-playasia](https://clawhub.ai/user/tom-playasia)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to search Play-Asia's catalog, check product prices and stock, buy digital products, retrieve order details and codes, and manage customer service tickets from an agent.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can spend wallet funds, expose order codes, and mutate customer service tickets when configured with a purchase-capable PA_TOKEN.

Mitigation: Use a read-only PA_TOKEN by default, enable purchase scope only intentionally, and require explicit itemized user confirmation before purchases or support-ticket actions.

Risk: Changing PA_BASE_URL while using real credentials could send account tokens to an unintended origin.

Mitigation: Keep PA_BASE_URL pointed at the official Play-Asia origin when real credentials are configured.

Risk: Unpinned npx execution can run a package version the user has not reviewed.

Mitigation: Verify the package and version before installation or run a pinned, reviewed package version.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/tom-playasia/skills/playasia)
- [Play-Asia L402 API](https://www.play-asia.com/l402)
- [Play-Asia access tokens](https://www.play-asia.com/account/access-tokens)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [JSON tool responses and Markdown guidance with inline shell and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Tool responses can include live product data, payment invoices, order details, digital delivery codes, wallet information, and customer service ticket data.]

## Skill Version(s):

0.3.0 (source: SKILL.md frontmatter and ClawHub release metadata; package.json reports 0.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
