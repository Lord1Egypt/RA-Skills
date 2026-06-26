## Description: <br>
Supports AI/ML talent discovery from lab pages, conference authors, GitHub networks, and public profiles, then structures candidate data and drafts personalized outreach. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[16miku](https://clawhub.ai/user/16miku) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Recruiters, sourcers, and research team operators use this skill to find AI/ML candidates from papers, lab pages, GitHub networks, and public profiles, structure and deduplicate candidate data, and generate personalized recruiting emails. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can collect personal data such as contact details, affiliations, research profiles, and candidate classifications at scale. <br>
Mitigation: Limit use to authorized recruiting workflows, collect only necessary public data, document the lawful basis for processing, and apply retention limits before exporting or sharing results. <br>
Risk: The artifact includes workflows for identifying Chinese candidates, which may create protected-attribute or proxy-attribute targeting risk. <br>
Mitigation: Disable ethnicity, nationality, or surname-based targeting unless reviewed and approved for a lawful, policy-compliant use case. <br>
Risk: Bulk outreach and Feishu table updates can expose scraped contact data to broad workspaces or trigger unsolicited messaging. <br>
Mitigation: Restrict Feishu permissions and workspace access, review generated messages before sending, and keep outreach volume and content within applicable platform, legal, and organizational policies. <br>
Risk: Scraping conference, lab, GitHub, LinkedIn, or other public sites may conflict with site terms, robots policies, or rate limits. <br>
Mitigation: Review each source's terms and robots policy, prefer official APIs where available, use conservative rate limits, and avoid scraping sources that disallow the intended use. <br>
Risk: External APIs and MCP services may require credentials with access to search, scraping, OpenReview, BrightData, or Feishu resources. <br>
Mitigation: Use the minimum required scopes, store credentials outside shared artifacts, rotate tokens regularly, and avoid embedding secrets in prompts, scripts, CSV files, or Feishu records. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/16miku/mapping-skill) <br>
- [Project link](https://github.com/16Miku/Mapping-Skill) <br>
- [README](artifact/README.md) <br>
- [Scripts README](artifact/scripts/README.md) <br>
- [Python scraping guide](artifact/references/python-scraping-guide.md) <br>
- [Anti-scraping solutions](artifact/references/anti-scraping-solutions.md) <br>
- [Conference paper scraping](artifact/references/conference-paper-scraping.md) <br>
- [Profile schema](artifact/references/profile-schema.md) <br>
- [Email templates](artifact/references/email-templates.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance, Files] <br>
**Output Format:** [Markdown, structured tables, CSV or spreadsheet-ready records, Python snippets, shell commands, and email drafts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create local CSV or Excel files and may update Feishu tables when the user provides authorized access.] <br>

## Skill Version(s): <br>
2.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
