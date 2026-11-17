## Description:

Search and browse eBay product listings across international marketplaces with filters for price, condition, buying format, seller location, sold or completed listings, and sorting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[linkfox-ai](https://clawhub.ai/user/linkfox-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External e-commerce sellers, buyers, and market researchers use this skill to search eBay listings, compare prices, inspect seller signals, and review active, sold, or completed listings across supported regional marketplaces.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review rates this release suspicious because it combines eBay search with feedback, account, credential, and payment flows.

Mitigation: Install only if comfortable using LinkFox as a paid intermediary for eBay searches, and review any onboarding or payment step before proceeding.

Risk: The skill uses LinkFox API keys and may guide users through phone/SMS account access.

Mitigation: Provide phone or SMS credentials only when intentionally creating or accessing a LinkFox account, and store API keys in a proper secret manager.

Risk: Automatic feedback reporting can send user intent or result details outside the search flow.

Mitigation: Review feedback payloads before sending and do not allow automatic feedback submission without user approval.

Risk: Saved response and cache files can contain sensitive searches, postal codes, or market research.

Mitigation: Periodically delete saved LinkFox response files and avoid searching sensitive terms when local persistence is not acceptable.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/linkfox-ai/skills/linkfox-ebay-search)
- [eBay Product Search API Reference](references/api.md)
- [Authentication and Credits Onboarding](references/onboarding.md)
- [LinkFox eBay Search API endpoint](https://tool-gateway.linkfox.com/ebay/search)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON parameters, shell commands, and saved JSON search responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Search responses may be saved as JSON files and summarized when large; cached search responses may be reused for 24 hours.]

## Skill Version(s):

1.0.6 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
