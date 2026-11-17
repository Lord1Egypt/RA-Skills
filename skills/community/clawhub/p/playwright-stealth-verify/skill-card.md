## Description:

Check whether a Playwright, Puppeteer, Selenium or CDP-driven browser presents a coherent fingerprint, using liarjs as a library against a Page you already have - navigator.webdriver, HeadlessChrome tokens, worker versus main-thread identity, patched-API integrity, WebGL versus WebGPU GPU identity.

This skill is ready for commercial/non-commercial use.

## Publisher:

[liarjsdev](https://clawhub.ai/user/liarjsdev)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and test engineers use this skill to measure whether an automated browser harness presents a coherent fingerprint and to add fingerprint-quality checks to Playwright, Puppeteer, Selenium, or CDP-based test suites.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installing or running the npm tool introduces normal supply-chain exposure.

Mitigation: Install only in a trusted project or disposable environment, and pin and review the exact liarjs version where practical.

Risk: Attaching to an existing browser or CDP endpoint can expose private sessions or browser state to the measurement process.

Mitigation: Confirm the endpoint with the user first, prefer a throwaway profile, and avoid profiles or CDP endpoints containing private sessions unless that is intentionally being measured.

Risk: Online scans contact an external endpoint to compare browser and network-layer signals.

Mitigation: Use --offline for JavaScript-only checks or point --endpoint at infrastructure you control for sensitive tests.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/liarjsdev/skills/playwright-stealth-verify)
- [liarjs hosted checker](https://liarjs.dev)
- [liarjs network endpoint](https://liarjs.dev/api/net.json)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with TypeScript and bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include browser fingerprint scan interpretation, pinned install commands, offline mode, or a custom endpoint for sensitive tests.]

## Skill Version(s):

1.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
