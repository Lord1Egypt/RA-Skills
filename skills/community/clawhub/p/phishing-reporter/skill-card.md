## Description: <br>
Report phishing, malware, and scam URLs to Google Safe Browsing, NCSC Switzerland, and other abuse reporting services. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xenofex7](https://clawhub.ai/user/xenofex7) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Security-minded users and operators use this skill to submit suspected phishing, malware, and scam URLs to abuse reporting services and to prepare manual fallback reports when automation is blocked. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Reports submit URLs and descriptions to external abuse-reporting services. <br>
Mitigation: Verify that the site is actually harmful, confirm each destination service, and avoid including unnecessary personal, internal, or contact details. <br>
Risk: Automated form submission can fail because of CAPTCHA, stateful wizards, or service-specific requirements. <br>
Mitigation: Use the bundled direct links, category guidance, and pre-written description template as a manual fallback. <br>


## Reference(s): <br>
- [Reporting Services Reference](references/services.md) <br>
- [Google Safe Browsing phishing report form](https://safebrowsing.google.com/safebrowsing/report_phish/?hl=en) <br>
- [NCSC Switzerland cyber incident reporting](https://www.report.ncsc.admin.ch/en/) <br>
- [Cloudflare phishing abuse report](https://abuse.cloudflare.com/phishing) <br>
- [PhishTank](https://phishtank.org/) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Markdown, Browser automation instructions] <br>
**Output Format:** [Markdown with URLs, report text templates, and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include manual reporting instructions and pre-written abuse report descriptions when automated submission fails.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
