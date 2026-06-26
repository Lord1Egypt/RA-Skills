## Description: <br>
Scrape government permit databases for B2B sales leads, enrich permit records with business emails via web scraping, and automate cold outreach. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[merjua14](https://clawhub.ai/user/merjua14) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External sales, marketing, insurance, POS, and service teams can use this skill to build prospect lists from public permit records and contact newly licensed businesses. Developers can adapt the included Node.js pipeline for specific state or county permit sources. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The pipeline can automatically send cold outreach emails to discovered contacts without a clear approval gate. <br>
Mitigation: Run with --dry-run first, inspect the generated CSV and recipient list, and add an explicit approval step before sending. <br>
Risk: Cold outreach and use of public permit data can trigger privacy, anti-spam, unsubscribe, suppression-list, and jurisdiction-specific compliance obligations. <br>
Mitigation: Confirm the applicable requirements for each campaign and jurisdiction, use verified sending domains, honor opt-outs, suppress bounces, and keep records of public-record data sources. <br>
Risk: A sending API key with broad limits could amplify mistakes in recipient selection or message content. <br>
Mitigation: Use a dedicated low-limit sending key and rate-limit outreach before increasing volume. <br>


## Reference(s): <br>
- [Government Permit Data Sources](references/data-sources.md) <br>
- [Cold Email Compliance](references/compliance.md) <br>
- [Texas TABC New Permits Issued](https://www.tabc.texas.gov/public-information/new-permits-issued/) <br>


## Skill Output: <br>
**Output Type(s):** [Code, Shell commands, Configuration, Files, Guidance] <br>
**Output Format:** [Markdown guidance with JavaScript, JSON configuration, shell commands, and CSV output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces a CSV lead list and may send outreach emails when configured with API keys and run without --dry-run.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
