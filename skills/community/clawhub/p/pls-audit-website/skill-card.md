## Description:

Perform comprehensive website health checks covering performance, broken links, security headers, accessibility, and SEO issues.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mattvalenta](https://clawhub.ai/user/mattvalenta)

### License/Terms of Use:


## Use Case:

Developers, site operators, and technical auditors use this skill to perform structured website health checks and produce actionable audit reports across performance, accessibility, security headers, SEO, and broken links.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Audit commands and URL-fetching snippets can create legal or operational risk if used against domains the operator is not authorized to test.

Mitigation: Run audits only against authorized domains from a low-privilege sandbox.

Risk: Installing or running third-party audit tools without pinned versions can introduce package and dependency risk.

Mitigation: Use pinned package versions or a locked dependency environment before executing examples.

Risk: URL-fetching snippets exposed directly to untrusted users could be abused to reach unintended internal or private network resources.

Mitigation: Add allowlists, redirect validation, private-network blocking, and timeouts before exposing these snippets in automated services.

## Reference(s):

- [PLS Website Audit on ClawHub](https://clawhub.ai/mattvalenta/skills/pls-audit-website)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Code, Markdown]

**Output Format:** [Markdown guidance with inline shell and Python code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces website audit checklists, command examples, code snippets, and a Markdown report template.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
