## Description: <br>
Hotel price comparison and deal-finding skill for Booking, Agoda, Google Hotels, and OpenTravel searches by city, travel dates, and guest count. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cotghw](https://clawhub.ai/user/cotghw) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Travel shoppers and agents use this skill to compare hotel prices and deal tiers across multiple booking sources for a requested city, date range, and adult guest count. It is intended to return ready-to-send Markdown deal cards rather than manually browsing each hotel site. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Hotel search details are sent to external travel providers and an exchange-rate service. <br>
Mitigation: Use the skill only for searches where sharing city, dates, guest count, locale, and related query details with those services is acceptable. <br>
Risk: Locale, market, currency conversion, taxes, and provider availability can affect displayed rates. <br>
Mitigation: Review or override the locale before running searches when market-specific pricing or taxes matter, and treat partial provider coverage as expected. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/cotghw/pricewin-deal-finder) <br>
- [PriceWin skills hub homepage](https://github.com/Price-Win/pricewin-skills-hub) <br>
- [OpenTravel API base URL](https://api.opentravel.one) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown deal cards with inline hyperlinks and price rows] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs compare hotel nightly prices in USD and may include partial source coverage when a provider has no inventory or is blocked.] <br>

## Skill Version(s): <br>
0.8.3 (source: server evidence, SKILL.md frontmatter, package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
