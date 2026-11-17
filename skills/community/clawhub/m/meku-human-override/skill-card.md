## Description:

Run safe, no-key MEKU Human Cloud MCP connection checks and use a clear REVOKE, REPLAY, PARTITION test checklist to assess human control in a local agent sandbox. Generates an evidence-based report without claiming a security certification.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mekusimeku](https://clawhub.ai/user/mekusimeku)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to check MEKU Human Cloud's public MCP metadata and to assess an agent's response to revoked, replayed, or unverifiable authority in an isolated synthetic test. It helps them record observed evidence without presenting a test plan or handshake as a security certification.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Public MCP checks contact an external service, and endpoint behavior may change.

Mitigation: Make checks only when requested, use the fixed public endpoint, send no credentials, and report observed results without retrying or claiming unobserved fields.

Risk: A synthetic challenge or successful public handshake could be mistaken for proof that a deployed agent enforces human authority.

Mitigation: Use only an isolated adapter with fake in-memory actions; report unrun cases as NOT_RUN and state that simulator results do not certify production behavior.

Risk: The supplied security scan has medium confidence because some references could not be resolved.

Mitigation: Consider that uncertainty before installation and review the linked source and challenge materials.

## Reference(s):

- [Server-resolved skill provenance](https://github.com/mekusimeku/meku-si/tree/main/skills/meku-human-override)
- [MEKU Human Cloud source repository](https://github.com/mekusimeku/meku-si)
- [Public MCP endpoint](https://meku.farm/api/public/mcp)
- [MEKU MCP lab](https://meku.farm/mcp-lab.html)
- [MEKU First Contact](https://meku.farm/first-contact.html)
- [Human Override Challenge specification](https://github.com/mekusimeku/meku-si/tree/main/skills/meku-human-override/references/challenge.md)
- [Evidence report template](https://github.com/mekusimeku/meku-si/tree/main/skills/meku-human-override/references/report-template.json)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Guidance]

**Output Format:** [Evidence-based Markdown report or JSON report based on the supplied template]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Records observed outcomes as PASS, FAIL, or NOT_RUN; a test specification or public handshake is not certification or proof of production safety.]

## Skill Version(s):

0.1.0 (source: ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
