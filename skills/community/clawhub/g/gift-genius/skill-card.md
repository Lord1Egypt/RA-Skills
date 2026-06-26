## Description: <br>
Gift Genius helps users choose Valentine's and relationship gifts by routing location, budget, recipient, and category preferences to merchant searches and returning a small set of curated recommendations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[evoleinik](https://clawhub.ai/user/evoleinik) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users use this skill to find gift options for partners, family, friends, and other recipients across flowers, chocolates, jewelry, watches, candles, fragrances, grooming, and supplements. The skill narrows choices by location, budget, recipient, and occasion, then returns concise recommendations with product or checkout links. <br>

### Deployment Geography for Use: <br>
Global, with merchant-specific routing for the USA, Singapore, Australia, Malaysia, and Europe/global supplement options. <br>

## Known Risks and Mitigations: <br>
Risk: The release is broader than a simple Valentine's flower finder and may guide users across multiple merchants and gift categories. <br>
Mitigation: Install only when a broad multi-merchant shopping assistant is intended, and review the supported merchant categories before use. <br>
Risk: The skill can propose checkout or cart-link actions. <br>
Mitigation: Require explicit user confirmation before any checkout, cart-link, or purchase-related action. <br>
Risk: Location routing can produce unsuitable recommendations if region is inferred incorrectly. <br>
Mitigation: Confirm the user's delivery region instead of relying only on inferred location. <br>
Risk: Calendar-based prompts could make the skill proactive around Valentine's Day. <br>
Mitigation: Avoid calendar-based prompts unless the user intentionally grants that behavior. <br>


## Reference(s): <br>
- [Gift Genius on ClawHub](https://clawhub.ai/evoleinik/gift-genius) <br>
- [AirShelf search API endpoint](https://dashboard.airshelf.ai/api/search?q=QUERY&merchant_ids=MERCHANT_ID&min_price=MIN&max_price=MAX&limit=5) <br>
- [AirShelf checkout API endpoint](https://dashboard.airshelf.ai/api/merchants/MERCHANT_ID/checkout) <br>
- [AirShelf compare API endpoint](https://dashboard.airshelf.ai/api/compare?products=ID1,ID2) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown recommendations with inline shell commands and product or checkout links] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl; uses merchant search, comparison, and checkout endpoints.] <br>

## Skill Version(s): <br>
4.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
