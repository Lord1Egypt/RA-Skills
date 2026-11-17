## Description:

Search ThreatFox for IP addresses, domains, URLs, and file hashes through an OOMOL-connected account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Security analysts and developers can check whether an IP address, domain, URL, or file hash appears in ThreatFox and review its threat type, malware family, and confidence when available.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup can introduce persistent changes to other agent skills without explaining those effects.

Mitigation: Review the CLI installation and its agent-skill changes before use; prefer a verified, fixed release. Consider setting OO_SKILLS_SYNC_DISABLED=1 before invoking oo if automatic skill synchronization is not wanted.

Risk: Indicator data sent to the connected service may contain information the user is not authorized to disclose externally.

Mitigation: Send only indicators you are authorized to disclose externally.

## Reference(s):

- [ThreatFox](https://threatfox.abuse.ch)
- [ThreatFox API documentation](https://threatfox.abuse.ch/api/)
- [oo CLI](https://github.com/oomol-lab/oo-cli)
- [ClawHub skill page](https://clawhub.ai/oomol/skills/oo-threatfox)

## Skill Output:

**Output Type(s):** [JSON, Text]

**Output Format:** [JSON lookup results with a concise text summary]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include IOC matches, threat type, malware family, confidence, or a not-found result.]

## Skill Version(s):

1.0.2 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
