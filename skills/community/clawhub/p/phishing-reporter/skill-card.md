## Description:

Report phishing, malware, and scam URLs to Google Safe Browsing, NCSC (Swiss Cyber Security), and other abuse reporting services.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xenofex7](https://clawhub.ai/user/xenofex7)

### License/Terms of Use:

MIT-0

## Use Case:

External users and security practitioners use this skill to report suspected phishing, malware, or scam URLs to abuse-reporting services and to prepare fallback manual reporting instructions when automation is blocked.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can submit consequential abuse reports to external organizations.

Mitigation: Review the exact URL, hostname, category, destination service, and report text before any submission.

Risk: Reports may include user-provided descriptions or contact details.

Mitigation: Avoid including private details unless they are necessary for the report.

Risk: Registrar reporting may require deriving a domain from user input.

Mitigation: Prefer a web WHOIS/RDAP lookup or a safely parsed hostname rather than passing raw user input to a shell command.

## Reference(s):

- [Reporting Services Reference](references/services.md)
- [Google Safe Browsing phishing report form](https://safebrowsing.google.com/safebrowsing/report_phish/?hl=en)
- [NCSC Switzerland reporting portal](https://www.report.ncsc.admin.ch/en/)
- [NCSC Switzerland phishing website chat path](https://www.report.ncsc.admin.ch/en/chat?path=406%3E407%3E1%3E128%3E132%3E133%3E314%3E130%3E135)
- [Cloudflare phishing abuse form](https://abuse.cloudflare.com/phishing)
- [PhishTank](https://phishtank.org/)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown with reporting links, browser automation steps, shell command suggestions, and prepared report text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May submit URLs, descriptions, and contact details to external abuse-reporting organizations.]

## Skill Version(s):

1.1.0 (source: server evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
