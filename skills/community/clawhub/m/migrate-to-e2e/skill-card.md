## Description:

Guides developers through migrating an existing automated test suite to e2e one tested slice at a time while keeping the source suite running and tracking progress in `MIGRATION.md`.

This skill is ready for commercial/non-commercial use.

## Publisher:

[e2e](https://clawhub.ai/user/e2e)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and test engineers use this skill to move an existing Playwright, Cypress, Selenium, Appium, Detox, Maestro, or TesterArmy suite to e2e in small, verified slices while keeping both suites running during migration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unpinned `npx` installers may resolve to changed packages, and the scan reports incomplete reference coverage.

Mitigation: Review installer commands and package sources, pin e2e to a reviewed version, and verify referenced documentation before installing or running commands.

## Reference(s):

- [e2e migration guide](https://e2e.com/docs/migrate)
- [Playwright migration guide](https://e2e.com/docs/migrate/playwright.md)
- [Cypress migration guide](https://e2e.com/docs/migrate/cypress.md)
- [Selenium migration guide](https://e2e.com/docs/migrate/selenium.md)
- [Appium migration guide](https://e2e.com/docs/migrate/appium.md)
- [Detox migration guide](https://e2e.com/docs/migrate/detox.md)
- [Maestro migration guide](https://e2e.com/docs/migrate/maestro.md)
- [TesterArmy migration guide](https://e2e.com/docs/migrate/testerarmy.md)
- [e2e web guide](https://e2e.com/docs/web.md)
- [e2e mobile guide](https://e2e.com/docs/mobile.md)

## Skill Output:

**Output Type(s):** [Code, Shell commands, Markdown, Guidance]

**Output Format:** [Markdown with code snippets and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Varies with the source suite; includes migrated test slices and a MIGRATION.md progress record.]

## Skill Version(s):

1.0.4 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
