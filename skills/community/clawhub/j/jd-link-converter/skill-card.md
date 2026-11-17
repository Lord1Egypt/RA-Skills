## Description:

Converts JD mobile share short links and mobile product links into clean desktop item.jd.com product links.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mousounikki](https://clawhub.ai/user/mousounikki)

### License/Terms of Use:

MIT

## Use Case:

Developers, ecommerce operators, and agents use this skill to convert JD short links, mobile product URLs, PC URLs with tracking parameters, or product IDs into canonical desktop JD product URLs. Short-link conversion may make outbound requests to resolve redirects; direct product links and product IDs can be converted locally.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Short-link resolution can follow redirects to unvalidated network destinations.

Mitigation: Install only where outbound requests to resolve JD short links are acceptable; prefer direct item.jd.com or item.m.jd.com URLs or product IDs in sensitive environments.

Risk: Short-link resolution may be unsuitable in environments where the agent can reach internal services.

Mitigation: Avoid running the resolver with access to internal networks unless redirect validation or egress controls are added.

Risk: Expired, blocked, or UA-sensitive short links may fail to resolve to a product page.

Mitigation: Ask for a mobile product link, desktop product link, or product ID when short-link resolution times out or redirects to the JD homepage.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mousounikki/skills/jd-link-converter)
- [JD URL formats](references/url_formats.md)
- [CSDN short-link reference](https://blog.csdn.net/Firewall5788/article/details/120301954)
- [OpenClaw skill reference](https://github.com/momozi1996/awesome-ai-persona-skills)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown table or JSON-style conversion results with canonical JD desktop URLs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include original URL, resolved URL, product ID, clean PC URL, and error text for failed conversions.]

## Skill Version(s):

1.1.0 (source: frontmatter and pyproject.toml)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
