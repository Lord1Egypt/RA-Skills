## Description: <br>
Scrape.do helps agents fetch public web pages as HTML or JSON, capture rendered screenshots, and inspect Scrape.do account usage through the OOMOL oo CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to run Scrape.do read-oriented scraping actions through an OOMOL-connected account for public page retrieval, JSON scrape output, screenshots, and account usage checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires an OOMOL-connected Scrape.do account and may rely on sensitive credentials managed by OOMOL. <br>
Mitigation: Use it only with an approved OOMOL account, avoid exposing raw tokens, and follow the setup flow only when authentication or connection errors occur. <br>
Risk: First-time setup can install the OOMOL oo CLI from a remote installer. <br>
Mitigation: Review the installer source and organization policy before running the install command. <br>
Risk: Scraping public pages can still be subject to website terms, legal restrictions, access controls, and billing limits. <br>
Mitigation: Confirm authorization and site terms before scraping, and monitor Scrape.do account usage or billing errors. <br>


## Reference(s): <br>
- [Scrape.do homepage](https://scrape.do) <br>
- [OOMOL oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [ClawHub skill page](https://clawhub.ai/oomol/oo-scrape-do) <br>
- [OOMOL publisher profile](https://clawhub.ai/user/oomol) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, JSON, Markdown, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON payloads or responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May return raw HTML, parsed JSON-friendly scrape results, base64 screenshots, account usage details, or setup guidance.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
