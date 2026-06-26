## Description: <br>
Personal Shopper is a multi-agent product and service research skill for Saudi Arabia that compares options, verifies prices and sources, and produces an Arabic HTML recommendation report. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Abdullah4AI](https://clawhub.ai/user/Abdullah4AI) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users use this skill to research product or service purchases in Saudi Arabia, compare ranked options, check prices, coupons, delivery, warranty, and return terms, and receive a clear Arabic recommendation report. <br>

### Deployment Geography for Use: <br>
Saudi Arabia, with a Riyadh focus <br>

## Known Risks and Mitigations: <br>
Risk: Generated shopping recommendations may contain stale prices, unavailable items, or seller claims that changed after research. <br>
Mitigation: Verify seller reputation, warranty, delivery, return terms, and current price before acting on generated links. <br>
Risk: The skill is intended for shopping research, not purchase authorization or account activity. <br>
Mitigation: Do not provide store logins, payment details, banking information, or unnecessary personal data. <br>
Risk: Remote fonts or product images can disclose network activity when privacy-sensitive or offline reporting is required. <br>
Mitigation: Remove or localize Google Fonts and avoid remote product images for privacy-sensitive or offline reports. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Abdullah4AI/personal-shopper) <br>
- [Brand Guideline](references/brand-guideline.md) <br>
- [Diamond Search Methodology](references/diamond-methodology.md) <br>
- [Market Dynamics - Saudi Arabia](references/market-dynamics.md) <br>
- [Anti-Bias Playbook](references/anti-bias-playbook.md) <br>
- [Domain Expertise Layer](references/domain-expertise.md) <br>
- [HTML Report Template](references/html-template.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Arabic RTL HTML report saved under shopping-reports/, with structured research summaries and source URLs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports include three ranked options, pricing evidence, coupons or cashback when found, scoring rationale, and purchase guidance; screenshots may be embedded when captured from allowed product pages.] <br>

## Skill Version(s): <br>
2.0.3 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
