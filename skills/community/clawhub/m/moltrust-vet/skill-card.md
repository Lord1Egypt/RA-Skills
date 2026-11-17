## Description:

Check any agent skill against ten versioned, CWE-mapped security checks before you install it, and get a verdict a third party can recompute.

This skill is ready for commercial/non-commercial use.

## Publisher:

[moltycel](https://clawhub.ai/user/moltycel)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to vet a candidate agent skill before installation by requesting a MolTrust audit and reporting the score, findings, auditor version, skill hash, and trust score.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Target repository URLs are sent to MolTrust for analysis.

Mitigation: Use the skill only with repository URLs that are acceptable to disclose to MolTrust; avoid private or internal repositories unless that sharing is approved.

Risk: The artifact contains inconsistent license statements.

Mitigation: Rely on the server-published MIT-0 license and LICENSE file for this release, and have the publisher align remaining documentation before users depend on the license statement.

Risk: Optional identity registration can create local private key material.

Mitigation: Treat registration as optional and store any generated private key only in the host's normal secret storage.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/moltycel/skills/moltrust-vet)
- [MolTrust skill homepage](https://moltrust.ch/skills.html)
- [MolTrust audit checks](https://api.moltrust.ch/guard/audit/checks)
- [MolTrust audit version](https://api.moltrust.ch/guard/audit/version)

## Skill Output:

**Output Type(s):** [guidance, shell commands, markdown, API calls, analysis]

**Output Format:** [Markdown with inline shell commands and API response summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports audit score, pass status, findings, auditor version, canonical skill hash, and ecosystem trust score when available.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
