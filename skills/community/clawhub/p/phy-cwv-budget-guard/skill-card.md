## Description:

Core Web Vitals budget enforcer that runs Lighthouse against a local dev server or staging URL, extracts LCP, INP, CLS, FCP, and TTFB scores, compares against a project .cwv-budget.json config, and fails CI if any metric regresses.

This skill is ready for commercial/non-commercial use.

## Publisher:

[phy041](https://clawhub.ai/user/phy041)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and frontend engineers use this skill to audit local or staging pages for Core Web Vitals regressions, compare results against project budgets, and receive fix recommendations before changes ship.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill's documented workflow can execute unpinned npm packages in local or CI environments.

Mitigation: Pin Lighthouse and related packages in the project lockfile and prefer local binaries over ad hoc npx downloads.

Risk: Headless browser commands and CI audits may run in environments that contain production secrets.

Mitigation: Run audits in isolated CI jobs without production secrets, validate target URLs, and avoid --no-sandbox unless the environment is already isolated.

## Reference(s):

- [Canlah AI Homepage](https://canlah.ai)
- [ClawHub Skill Page](https://clawhub.ai/phy041/skills/phy-cwv-budget-guard)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline JSON, Python, HTML, YAML, and bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May append local Core Web Vitals history and may propose CI commands that fail a build on budget regression.]

## Skill Version(s):

1.0.3 (source: server release metadata and artifact metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
