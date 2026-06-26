## Description: <br>
Guides agents through technical SEO indexing fixes for Google Search Console issues, noindex decisions, and Google Indexing API setup. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kostja94](https://clawhub.ai/user/kostja94) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, technical SEO practitioners, and site operators use this skill to triage Google Search Console indexing statuses and choose concrete fixes such as canonical updates, noindex directives, robots.txt adjustments, URL inspection, or Indexing API setup. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Incorrect noindex, canonical, robots.txt, redirect, or indexing API changes can reduce search visibility for important pages. <br>
Mitigation: Review each affected URL and its intended search behavior before applying the recommended change. <br>
Risk: Google Indexing API setup may expose credentials if service account details are pasted into project context files. <br>
Mitigation: Use a dedicated service account scoped to the relevant Search Console property and keep credentials outside shared context files. <br>


## Reference(s): <br>
- [Google Search Central: Page indexing report](https://support.google.com/webmasters/answer/7440203) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Configuration] <br>
**Output Format:** [Markdown action items with tables and inline configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [No executable code; recommendations may affect search visibility and should be reviewed per URL.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
