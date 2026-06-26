## Description: <br>
Scans GitHub for potential AI company customer leads by searching AI/ML repositories, large model projects, and training code, then filtering by stars, activity, and company signals. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dashiming](https://clawhub.ai/user/dashiming) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and sales or growth teams use this skill to discover GitHub repositories and organizations that may indicate AI infrastructure demand. It can search and filter repositories, enrich organization details, and export lead lists for review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Exported lead files can contain sensitive business or contact data. <br>
Mitigation: Use enrichment and CSV export only for appropriate lawful purposes, restrict access to exported files, and store or delete them according to the user's data handling policy. <br>
Risk: A broad GitHub token could expose more access than the skill needs. <br>
Mitigation: Use the least-privileged GitHub token available, prefer tokens limited to public metadata access, and avoid passing long-lived credentials unnecessarily. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/dashiming/pans-github-scout) <br>
- [GitHub REST API](https://api.github.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, CSV, shell commands] <br>
**Output Format:** [Terminal table, JSON array, or CSV export file] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May call the GitHub API with an optional GITHUB_TOKEN; CSV exports can include repository, owner, organization, location, blog, and email fields when enrichment is enabled.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
