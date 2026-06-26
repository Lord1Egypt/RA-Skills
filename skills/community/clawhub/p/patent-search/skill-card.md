## Description: <br>
Patent search and analytics via 9235 API (search, detail, claims, company portrait, Excel export). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[windinwing](https://clawhub.ai/user/windinwing) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and patent analysts use this skill to query and analyze patent/IP records through the 9235 API, inspect details and legal/citation data, and export result or analytics files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Patent/IP search queries, identifiers, and filters are sent to the 9235 service with the user's API token. <br>
Mitigation: Use only if that data sharing is acceptable, review the provider's terms and privacy policy, and protect or rotate PATENT_API_TOKEN as a secret. <br>
Risk: Export behavior may automatically install openpyxl or python-docx if they are not already available. <br>
Mitigation: Run in an isolated environment or preinstall vetted dependency versions before enabling export workflows. <br>
Risk: Export and download commands can create local files. <br>
Mitigation: Configure output directories deliberately and review generated files before sharing or committing them. <br>


## Reference(s): <br>
- [9235 Open Platform](https://www.9235.net/api/open) <br>
- [9235 API](https://www.9235.net/api) <br>
- [9235 API Interface Documentation](https://www.9235.net/api/interface.html) <br>
- [9235 Search Help](https://www.9235.net/help/index.html) <br>
- [ClawHub patent-search Listing](https://clawhub.ai/windinwing/patent-search) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, files] <br>
**Output Format:** [Markdown/text responses with optional API result data and local Excel, CSV, or Markdown export files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires PATENT_API_TOKEN; sends patent/IP queries and identifiers to 9235 and may write export or download files locally.] <br>

## Skill Version(s): <br>
1.0.10 (source: server evidence, SKILL.md frontmatter, CHANGELOG) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
