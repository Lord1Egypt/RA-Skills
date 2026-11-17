## Description:

Full-featured OSINT reconnaissance using the MerkleMap API: subdomain enumeration, SSL/TLS certificate inspection, certificate deep-dive, real-time CT log monitoring, typosquatting detection, risk scoring, and professional HTML/JSON report generation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[laikhtman](https://clawhub.ai/user/laikhtman)

### License/Terms of Use:

MIT-0

## Use Case:

Security teams, OSINT analysts, developers, and infrastructure owners use this skill to investigate domains, audit SSL/TLS certificates, monitor certificate transparency activity, detect typosquatting, and generate reconnaissance reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Investigation targets are sent to the MerkleMap API.

Mitigation: Use only when sharing target domains with MerkleMap is acceptable for the investigation.

Risk: Generated reconnaissance reports may contain sensitive infrastructure findings.

Mitigation: Store HTML and JSON reports in private locations and avoid synced or public folders.

Risk: HTML reports may include untrusted certificate data.

Mitigation: Review or modify report generation to HTML-escape API-returned values before opening reports in a browser.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/laikhtman/skills/merklemap-osint)
- [MerkleMap API Documentation](https://www.merklemap.com/documentation)
- [MerkleMap API Key Profile](https://www.merklemap.com/user-profile/api)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown responses with optional HTML and JSON report files, API request guidance, and shell configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write sensitive reconnaissance reports to local HTML/JSON files when requested.]

## Skill Version(s):

3.0.1 (source: server release evidence and skill metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
