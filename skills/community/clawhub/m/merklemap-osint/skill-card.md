## Description: <br>
Full-featured OSINT reconnaissance using the MerkleMap API for subdomain enumeration, SSL/TLS certificate inspection, certificate deep dives, real-time CT log monitoring, typosquatting detection, risk scoring, and HTML/JSON report generation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[laikhtman](https://clawhub.ai/user/laikhtman) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Security teams, OSINT analysts, and developers use this skill to investigate domain attack surfaces, audit certificate transparency data, monitor newly issued certificates, and generate stakeholder-ready reconnaissance reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a MerkleMap API key. <br>
Mitigation: Store MERKLEMAP_API_KEY as a secret environment variable and avoid logging, echoing, or sharing it in agent output. <br>
Risk: OSINT and certificate-transparency scans can be sensitive when run against domains outside the user's scope. <br>
Mitigation: Use the skill only for domains the user is authorized or comfortable investigating. <br>
Risk: Generated HTML and JSON reports may persist reconnaissance results on disk. <br>
Mitigation: Store reports in an appropriate location, limit sharing, and remove them when they are no longer needed. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/laikhtman/merklemap-osint) <br>
- [MerkleMap API Documentation](https://www.merklemap.com/documentation) <br>
- [MerkleMap API Key Page](https://www.merklemap.com/user-profile/api) <br>
- [MerkleMap](https://www.merklemap.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, json, html, guidance] <br>
**Output Format:** [Markdown responses with optional self-contained HTML and JSON report files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include structured tables, risk scores, executive summaries, findings, and local report files when requested.] <br>

## Skill Version(s): <br>
3.0.1 (source: server release metadata and skill frontmatter metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
