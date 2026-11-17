## Description:

Personal Shopper is a multi-agent product and service research and recommendation skill for Saudi Arabia.

This skill is ready for commercial/non-commercial use.

## Publisher:

[abdullah4ai](https://clawhub.ai/user/abdullah4ai)

### License/Terms of Use:


## Use Case:

External users in Saudi Arabia use this skill to research products or local services, compare options by price, value, availability, and source trust, and receive three ranked recommendations in an Arabic RTL HTML report.

### Deployment Geography for Use:

Saudi Arabia, focused on Riyadh

## Known Risks and Mitigations:

Risk: Generated HTML reports can include web-sourced content that may be unsafe if inserted without escaping.

Mitigation: HTML-escape generated report content before rendering or saving the report.

Risk: Purchase links may lead outside expected retailers or use unsafe URL schemes.

Mitigation: Validate purchase URLs as HTTPS and restrict them to expected store domains before including them in a report.

Risk: Local screenshot embedding can expose unintended files if paths are not contained.

Mitigation: Resolve screenshot paths and only embed PNG files contained under shopping-reports/screenshots/.

Risk: External font or image requests in reports may be under-disclosed.

Mitigation: Remove external font and image requests or clearly disclose them before distribution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/abdullah4ai/skills/personal-shopper)
- [Anti-Bias Playbook](artifact/references/anti-bias-playbook.md)
- [Brand Guideline](artifact/references/brand-guideline.md)
- [Diamond Search v2 - Extended Agent Prompts](artifact/references/diamond-methodology.md)
- [Domain Expertise Layer](artifact/references/domain-expertise.md)
- [HTML Report Template](artifact/references/html-template.md)
- [Market Dynamics - Saudi Arabia](artifact/references/market-dynamics.md)

## Skill Output:

**Output Type(s):** [analysis, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Arabic RTL HTML report saved as a local .html file, with structured research summaries and ranked recommendations.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports are written under shopping-reports/ and may include validated local screenshots from shopping-reports/screenshots/.]

## Skill Version(s):

2.0.3 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
