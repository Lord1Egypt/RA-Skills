## Description: <br>
Drive CloakBrowser Manager stealth profiles with @playwright/cli over CDP for browser automation that needs a persistent logged-in session, anti-detect fingerprints, or Cloudflare challenge handling. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tenequm](https://clawhub.ai/user/tenequm) <br>

### License/Terms of Use: <br>
Apache 2.0 <br>


## Use Case: <br>
Developers and automation operators use this skill to connect Playwright CLI to running CloakBrowser Manager profiles, reuse logged-in browser state, inspect pages, and drive JS-heavy sites through CDP. It is intended for authorized browser automation where persistent sessions, proxy-aware profiles, or stealth browser behavior are required. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill enables stealth, logged-in browser automation that can access sensitive account data. <br>
Mitigation: Install only for accounts and sites you are authorized to access, and prevent the agent from returning cookies, tokens, full authenticated responses, or unrelated account data. <br>
Risk: Stealth profiles and challenge-handling workflows can be misused to bypass site controls or scrape protected services. <br>
Mitigation: Use the skill only for permitted automation, respect site access rules, and review planned commands before execution. <br>
Risk: The CloakBrowser Manager setup may run without authentication when bound locally or tunneled over SSH. <br>
Mitigation: Keep the Manager bound to localhost or protected by an SSH tunnel; use an authentication token and HTTPS reverse proxy if direct exposure is unavoidable. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/tenequm/skills/playwright-cli-cloakbrowser) <br>
- [CloakBrowser Manager](https://github.com/CloakHQ/CloakBrowser-Manager) <br>
- [CloakBrowser](https://github.com/CloakHQ/CloakBrowser) <br>
- [CloakBrowser project site](https://cloakbrowser.dev) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, code] <br>
**Output Format:** [Markdown with inline bash and JavaScript code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May instruct the agent to run playwright-cli, curl, and docker commands against local or tunneled CloakBrowser Manager endpoints.] <br>

## Skill Version(s): <br>
0.3.0 (source: frontmatter, changelog, server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
