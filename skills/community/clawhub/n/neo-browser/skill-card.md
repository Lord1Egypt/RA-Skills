## Description: <br>
Neo helps agents browse websites, read pages, interact with web apps, call website APIs, scrape data, and automate browser tasks through the Neo CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[4ier](https://clawhub.ai/user/4ier) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use Neo to inspect websites, read pages, discover captured web APIs, execute authenticated website API calls, and automate browser interactions when API access is not available. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Neo can use real Chrome sessions and cookies to call website APIs, post content, manage login state, replay requests, and run page JavaScript. <br>
Mitigation: Install only if you trust the @4ier/neo CLI with the browser profile in use, and require explicit approval before posting, API writes, cookie export/import/clear, request replay, or page JavaScript execution. <br>
Risk: Using a primary Chrome profile can expose sensitive accounts and browsing state to browser automation. <br>
Mitigation: Prefer a separate Chrome profile that contains only the accounts needed for the task, and avoid using the skill on sensitive sites. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/4ier/neo-browser) <br>
- [Neo npm Package](https://www.npmjs.com/package/@4ier/neo) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and CLI guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include browser automation steps, API call instructions, and safety checks for Neo and Chrome sessions.] <br>

## Skill Version(s): <br>
2.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
