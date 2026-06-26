## Description: <br>
Analyzes webpage HTML and interactive elements to help agents generate Selenium automation scripts for authorized pages. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[icestorms](https://clawhub.ai/user/icestorms) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and automation engineers use this skill to inspect public or explicitly authorized web pages, identify form controls and links, and draft Selenium scripts for tasks such as login, search, and form submission. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Page HTML captured for model analysis may include tokens, credentials, CSRF values, or other sensitive data. <br>
Mitigation: Use the skill only on public or explicitly authorized pages, avoid sensitive authenticated or internal systems, and redact HTML before sending it to any model. <br>
Risk: The page fetch script uses browser flags that can bypass normal certificate and automation safeguards. <br>
Mitigation: Run it only in controlled environments for intended Selenium inspection work, and do not rely on it for validating page trust or certificate status. <br>
Risk: Retained HTML files, including error captures, can preserve sensitive page content after analysis. <br>
Mitigation: Delete retained HTML outputs, including error_page.html, after review unless there is an explicit retention need. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/icestorms/html-to-selenium) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, guidance] <br>
**Output Format:** [Markdown with element inventories, notes, and Python Selenium code snippets.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include command examples and generated Selenium control scripts; captured HTML should be deleted or redacted after analysis.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
