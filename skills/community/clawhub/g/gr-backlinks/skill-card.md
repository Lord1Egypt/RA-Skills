## Description: <br>
Gr Backlinks helps indie founders plan systematic backlink-building campaigns across Wikipedia and Wikidata preparation, PR outreach, review-site listings, community participation, and backlink auditing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gingiris-1031](https://clawhub.ai/user/gingiris-1031) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External founders, growth operators, and marketing-focused agent users use this skill to choose backlink channels, prepare outreach and submission materials, and audit known backlinks for early-stage sites. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The optional audit script can make outbound requests to Common Crawl, known-link URLs, and DataForSEO when credentials are provided. <br>
Mitigation: Run the script manually, use only trusted known-link files, avoid localhost or private-network URLs, and provide DATAFORSEO_B64 only when paid DataForSEO queries are intended. <br>
Risk: Backlink outreach and public-promotion guidance can be misused for spam, fake reviews, or platform-policy violations. <br>
Mitigation: Use the artifact's disclosure, notability, and anti-pattern guidance: avoid purchased links, inauthentic reviews, multiple accounts, undisclosed paid Wikipedia editing, and promotional self-linking. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/gingiris-1031/gr-backlinks) <br>
- [Publisher Profile](https://clawhub.ai/user/gingiris-1031) <br>
- [HARO / Featured.com Response Template](artifact/gr-backlinks/templates/haro-response.md) <br>
- [Reddit + Quora Trust-Building Playbook](artifact/gr-backlinks/templates/reddit-quora.md) <br>
- [Wikipedia Article Preparation Template](artifact/gr-backlinks/templates/wikipedia-prep.md) <br>
- [Backlinks Audit Script](artifact/gr-backlinks/scripts/backlinks-audit.py) <br>
- [Wikipedia Articles for Creation](https://en.wikipedia.org/wiki/Wikipedia:Articles_for_creation) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration, JSON] <br>
**Output Format:** [Markdown guidance and templates with optional JSON output from the audit script] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The optional audit script accepts a target domain, an optional known-links file, and optional DataForSEO credentials.] <br>

## Skill Version(s): <br>
1.0.2 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
