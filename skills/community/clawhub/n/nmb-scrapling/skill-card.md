## Description:

Web scraping framework supporting anti-bot bypass, adaptive parsing, session and proxy management, large-scale crawling, and dynamic content extraction.

This skill is ready for commercial/non-commercial use.

## Publisher:

[superowl](https://clawhub.ai/user/superowl)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to install and operate Scrapling for website scraping, structured extraction, dynamic page rendering, session-based crawling, and site-change monitoring. It is intended for authorized collection workflows where the user controls target selection and compliance obligations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill supports anti-bot and Cloudflare-bypass scraping modes against arbitrary URLs.

Mitigation: Use those modes only for sites where access is authorized, and disable or avoid stealth and bypass options for routine collection.

Risk: Broad network fetching and proxy-enabled crawling can collect sensitive or unauthorized data at scale.

Mitigation: Run in an isolated environment with restricted network egress, review target lists before execution, and handle scraped data as potentially sensitive.

Risk: Unreviewed dependency changes could alter scraping behavior or browser automation behavior.

Mitigation: Pin reviewed dependency versions and scan the environment before deployment.

## Reference(s):

- [Scrapling documentation](https://scrapling.readthedocs.io)
- [Scrapling GitHub repository](https://github.com/D4Vinci/Scrapling)
- [ClawHub skill page](https://clawhub.ai/superowl/skills/nmb-scrapling)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Code, Configuration, Files]

**Output Format:** [Markdown with bash, Python, and JSON code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce local scrape outputs as JSON, text, Markdown, or HTML when the helper script is executed.]

## Skill Version(s):

1.0.0 (source: release evidence and artifact metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
