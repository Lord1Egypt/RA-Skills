## Description:

Produces a client site handoff report with live link-integrity evidence for launch or major-relaunch handoff gates.

This skill is ready for commercial/non-commercial use.

## Publisher:

[powmcp](https://clawhub.ai/user/powmcp)

### License/Terms of Use:

MIT

## Use Case:

External developers and site-launch leads use this skill to collect observed link-integrity evidence for a deployed public page, separate link findings from broader handoff checks, and produce a dated Markdown handoff report.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The remote PowMCP link-checking service receives the submitted page URL.

Mitigation: Submit only public, deployed URLs and avoid private, authenticated, or secret-bearing pages.

Risk: The MCP connection may remain available after the handoff review.

Mitigation: Remove the MCP connection after the review if the service should not be available in future sessions.

Risk: The link-integrity result covers one submitted page and at most 100 unique link and image targets.

Mitigation: Record the one-page and 100-target limits, report truncation, and run separate checks for other pages or launch-readiness areas.

Risk: Installer or source changes could matter in environments with strict supply-chain requirements.

Mitigation: Verify or pin the npx installer/source before installation when stronger supply-chain controls are required.

## Reference(s):

- [Broken Link Check Reference](artifact/references/broken-link-check.md)
- [Broken Link Check](https://powmcp.com/apps/broken-link-check/)
- [ClawHub Skill Page](https://clawhub.ai/powmcp/skills/produce-client-site-handoff-report)
- [PowMCP Broken Link Check MCP Endpoint](https://powmcp.com/broken-link-check/mcp)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown report with checklist-style findings and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes observed link-integrity counts, coverage limits, unresolved categories, verb-first fixes, and separate launch-check status when evidence is available.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
