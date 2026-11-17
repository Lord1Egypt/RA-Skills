## Description:

Run a comprehensive HubSpot CRM database audit. Analyzes contacts, companies, deals, engagement, data quality, and deliverability. Use when starting a CRM cleanup, onboarding a new client, or performing quarterly health checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tomgranot](https://clawhub.ai/user/tomgranot)

### License/Terms of Use:

MIT-0

## Use Case:

CRM administrators, consultants, and RevOps teams use this skill to audit a HubSpot portal across contacts, companies, deals, engagement, data quality, owner health, workflows, and pipeline hygiene. It helps produce a graded Markdown cleanup report with prioritized recommendations and an ordered follow-on skill prescription.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles a sensitive HubSpot private app token.

Mitigation: Use a dedicated least-privilege read-only token and provide it through a secure environment or secret store rather than saving it to .env.

Risk: Generated audit reports may contain sensitive CRM information.

Mitigation: Review the report before sharing it and store outputs according to the organization's CRM data handling requirements.

Risk: Dependency installation can introduce supply-chain or environment risk.

Mitigation: Install dependencies in an isolated environment with pinned versions.

Risk: The artifact describes optional follow-on actions that create skills, commit code, push to a fork, or open a pull request.

Mitigation: Do not allow those contribution actions unless the user explicitly starts that separate development workflow.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tomgranot/skills/hubspot-audit)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline bash and Python code blocks, plus generated Python and Markdown report files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces a dated HubSpot audit report, graded findings, prioritized recommendations, and suggested follow-on skills.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
