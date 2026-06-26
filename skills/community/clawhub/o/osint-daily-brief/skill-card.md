## Description: <br>
Generate a daily OSINT intelligence brief on a domain, company, IP, person, or keyword using Tavily web search, DNS recon, WHOIS, and optional Shodan enrichment. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[infectit007](https://clawhub.ai/user/infectit007) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Security teams, developers, and external analysts use this skill to assemble short OSINT briefs for authorized brand monitoring, competitive intelligence, pre-engagement reconnaissance, and daily threat awareness. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill gathers information about domains, companies, IPs, people, or keywords, which can create legal or policy risk when used on unauthorized targets. <br>
Mitigation: Use it only for assets, clients, brands, or targets that the operator is authorized to research. <br>
Risk: Queries and findings may be sent to external services such as Tavily, Shodan, or messaging delivery channels. <br>
Mitigation: Review API keys, scheduled jobs, Telegram or other delivery settings, and target sensitivity before enabling automated runs. <br>
Risk: Daily scheduled briefs can repeatedly disclose target names and findings if cron prompts or delivery channels are misconfigured. <br>
Mitigation: Confirm cron configuration and recipients before scheduling brand, competitor, or client monitoring. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/infectit007/osint-daily-brief) <br>
- [Publisher profile](https://clawhub.ai/user/infectit007) <br>
- [Tavily Search API endpoint](https://api.tavily.com/search) <br>
- [Shodan host lookup endpoint](https://api.shodan.io/shodan/host/{ip_or_domain}) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown brief with Python and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses a required TAVILY_API_KEY and optional SHODAN_API_KEY; local DNS and WHOIS enrichment depend on dig and whois being installed.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
