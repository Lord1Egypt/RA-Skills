## Description: <br>
Check Google indexed page counts for one or more domains using the "site:" search operator through Chrome Remote Debugging Protocol (CDP on localhost:9222), with single-domain results or comparison table output. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lgx-00](https://clawhub.ai/user/lgx-00) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, SEO practitioners, and site operators use this skill to estimate Google index coverage for one or more domains and compare results in a Markdown report. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Chrome remote debugging can expose browser cookies and logged-in session state when connected to a normal browser profile. <br>
Mitigation: Run Chrome with a dedicated temporary user-data directory, avoid personal logins, and connect only to that isolated debugging session. <br>
Risk: Cleanup that targets the wrong browser context could close unrelated tabs. <br>
Mitigation: Track the created target ID and close only the tab created for the check, then verify the remaining CDP tab list. <br>
Risk: Google site: operator counts are approximate and can vary by data center or page state. <br>
Mitigation: Present counts as estimates and use Google Search Console when precise indexing data is required. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lgx-00/google-index-checker) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Code, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and JavaScript snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces approximate Google site: operator counts, with single-domain text output or a multi-domain comparison table.] <br>

## Skill Version(s): <br>
1.1.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
