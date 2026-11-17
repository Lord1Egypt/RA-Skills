## Description:

Generate a daily OSINT intelligence brief on a domain, company, IP, person, or keyword using Tavily web search, DNS records, WHOIS, and optional Shodan data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[infectit007](https://clawhub.ai/user/infectit007)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, security analysts, and operators use this skill to assemble concise OSINT briefs for brand monitoring, competitive intelligence, pre-engagement reconnaissance, and daily threat awareness.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: OSINT targets and search terms may be sent to third-party providers such as Tavily and Shodan.

Mitigation: Use the skill only for targets appropriate for those services, and avoid submitting sensitive internal identifiers unless disclosure to those providers is acceptable.

Risk: Scheduled monitoring can create recurring collection and report-forwarding jobs.

Mitigation: Review cron prompts, recipients, and monitored targets before enabling scheduled runs, and disable jobs that are no longer authorized.

Risk: Reconnaissance activity can cross legal or authorization boundaries if used on targets without permission.

Mitigation: Run the skill only against owned assets, explicitly authorized engagements, or investigations permitted by applicable law and policy.

## Reference(s):

- [OSINT Daily Brief ClawHub listing](https://clawhub.ai/infectit007/skills/osint-daily-brief)
- [Tavily Search API endpoint](https://api.tavily.com/search)
- [Shodan Host API endpoint](https://api.shodan.io/shodan/host/{ip_or_domain})

## Skill Output:

**Output Type(s):** [Markdown, Analysis, Code, Shell commands, Configuration]

**Output Format:** [Structured Markdown brief with example Python and shell command blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires TAVILY_API_KEY; SHODAN_API_KEY, dig, whois, and scheduled cron delivery are optional.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
