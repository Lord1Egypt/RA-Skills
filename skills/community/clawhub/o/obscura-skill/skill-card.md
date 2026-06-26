## Description: <br>
Obscura Skill guides agents through using Obscura for JavaScript-heavy web scraping, headless browser automation, CDP integrations, and frontend E2E testing with Puppeteer or Playwright. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[felipeoff](https://clawhub.ai/user/felipeoff) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering agents use this skill to install and configure Obscura, choose fetch/scrape/serve workflows, connect Puppeteer or Playwright over CDP, and run frontend E2E checks with lower browser overhead. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security summary flags broad guidance toward stealth anti-bot scraping without clear authorization checks. <br>
Mitigation: Use stealth or anti-detection modes only where the operator has explicit permission and policy or legal clearance. <br>
Risk: Browser automation can interact with authenticated sessions or third-party websites. <br>
Mitigation: Avoid production credentials, respect site policies and robots controls, and use test accounts or scoped credentials where possible. <br>
Risk: A CDP server exposes browser control while it is running. <br>
Mitigation: Bind the CDP server to localhost, stop it after use, and avoid exposing the port beyond the local machine. <br>
Risk: Installing or running browser binaries can introduce supply-chain risk. <br>
Mitigation: Prefer pinned or verified Obscura binaries and install them with the least privilege needed. <br>


## Reference(s): <br>
- [Obscura Skill on ClawHub](https://clawhub.ai/felipeoff/obscura-skill) <br>
- [Obscura upstream repository](https://github.com/h4ckf0r0day/obscura) <br>
- [Obscura releases](https://github.com/h4ckf0r0day/obscura/releases) <br>
- [Chrome DevTools Protocol](https://chromedevtools.github.io/devtools-protocol/) <br>
- [Puppeteer documentation](https://pptr.dev/) <br>
- [Playwright documentation](https://playwright.dev/) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with inline shell, JavaScript, TypeScript, JSON, and YAML snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include commands that install or run Obscura, patch Playwright configuration, and start a localhost CDP server.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
