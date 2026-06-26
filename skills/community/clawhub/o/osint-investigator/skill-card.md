## Description: <br>
Deep OSINT investigations that classify a target and gather publicly available information across web search, social media, DNS/WHOIS, image search, maps, public records, and related sources into a structured intelligence report. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cineglobe](https://clawhub.ai/user/cineglobe) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users, analysts, and developers use this skill for authorized open-source intelligence investigations of people, usernames, domains, IP addresses, organizations, phone numbers, email addresses, locations, images, and other public targets. It helps plan multi-source searches, correlate findings, and produce a structured report with sources, confidence, and gaps. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill gives the agent broad profiling authority over people and other targets. <br>
Mitigation: Use it only for lawful, authorized, and clearly scoped investigations, and avoid investigating private individuals without consent or another clear lawful basis. <br>
Risk: The skill asks users to provide and store sensitive platform credentials and API keys. <br>
Mitigation: Prefer limited-scope API tokens stored outside chat, avoid personal account passwords, and keep any local configuration file permission-restricted. <br>
Risk: The PDF wrapper can install the fpdf2 dependency before generating reports. <br>
Mitigation: Run PDF generation only in an isolated environment where dependency installation behavior is acceptable. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/cineglobe/osint-investigator) <br>
- [OSINT Sources - Master Reference](references/osint-sources.md) <br>
- [Social Platforms Reference](references/social-platforms.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Structured Markdown report with optional shell commands, configuration updates, and optional PDF output from Markdown] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May optionally create a local JSON configuration file and PDF report when the user enables those features.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
