## Description:

Production-grade Playwright testing toolkit for AI coding agents.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thangcq0310](https://clawhub.ai/user/thangcq0310)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and QA engineers use this skill to set up Playwright, generate and review end-to-end tests, diagnose flaky failures, migrate Cypress or Selenium suites, and work with optional TestRail and BrowserStack integrations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Credentialed TestRail, BrowserStack, or reporting integrations can send data to external services.

Mitigation: Keep optional integrations disabled unless needed, use low-privilege tokens, verify destination URLs before reporting, and avoid production-like data in test output.

Risk: Generated tests, configuration, or reports may modify repositories where browser testing is not expected.

Mitigation: Install only in repositories where running Playwright tests and writing test assets is acceptable, and review generated file changes before committing.

Risk: Unpinned Playwright or TypeScript execution can pull unexpected dependency versions.

Mitigation: Prefer lockfile-pinned local Playwright and tsx invocations over bare npx.

## Reference(s):

- [Playwright Pro README](README.md)
- [Golden Rules](reference/golden-rules.md)
- [Locator Guidance](reference/locators.md)
- [Assertion Guidance](reference/assertions.md)
- [Fixture Guidance](reference/fixtures.md)
- [Flaky Test Guidance](reference/flaky-tests.md)
- [Test Template Index](templates/README.md)
- [Cypress Migration Mapping](skills/migrate/cypress-mapping.md)
- [Selenium Migration Mapping](skills/migrate/selenium-mapping.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline code and shell command blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write Playwright test files, configuration, CI snippets, reports, and integration setup guidance when the host agent executes the skill.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
