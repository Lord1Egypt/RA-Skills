## Description:

Obscura Skill guides agents through web scraping, headless browser automation, and Playwright or Puppeteer E2E testing with the Obscura CDP-compatible browser.

This skill is ready for commercial/non-commercial use.

## Publisher:

[felipeoff](https://clawhub.ai/user/felipeoff)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to choose Obscura CLI and CDP workflows for JavaScript-heavy scraping, browser automation, and frontend E2E validation. It provides installation, command, Playwright, Puppeteer, and operational guidance for authorized use.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installing unverified latest binaries with elevated privileges can introduce supply-chain or local privilege risk.

Mitigation: Use a pinned Obscura release with published checksums or signatures, and install in a user-local directory instead of using sudo where possible.

Risk: Stealth scraping and browser automation can violate site terms, robots policies, or internal authorization requirements.

Mitigation: Use stealth and scraping features only on sites and systems where the operator has authorization and policy approval.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/felipeoff/skills/obscura-skill)
- [Obscura upstream repository](https://github.com/h4ckf0r0day/obscura)
- [Obscura releases](https://github.com/h4ckf0r0day/obscura/releases)
- [Chrome DevTools Protocol](https://chromedevtools.github.io/devtools-protocol/)
- [Puppeteer](https://pptr.dev/)
- [Playwright](https://playwright.dev/)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with inline code blocks and command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include installation commands, Playwright or Puppeteer snippets, and policy cautions for scraping and stealth use.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
