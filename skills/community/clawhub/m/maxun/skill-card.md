## Description: <br>
List and run Maxun web scraping robots. Use when asked to list robots, run a robot, scrape a website, or get robot results. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rohitr311](https://clawhub.ai/user/rohitr311) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to list Maxun robots, run web scraping jobs, inspect previous runs, fetch run results, and abort active robot runs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security review reports broad no-confirmation shell access and under-disclosed state-changing or local execution risks. <br>
Mitigation: Review before installing, keep command confirmations enabled, and avoid granting global full-shell permissions. <br>
Risk: The helper can load environment variables from a local .env file before calling Maxun API endpoints. <br>
Mitigation: Set MAXUN_API_KEY through a trusted environment and do not run the skill from directories with untrusted .env files. <br>
Risk: The abort command can change the state of an active Maxun robot run. <br>
Mitigation: Treat abort as a sensitive action and require explicit user approval before execution. <br>


## Reference(s): <br>
- [Maxun homepage](https://www.maxun.dev) <br>
- [Maxun app](https://app.maxun.dev) <br>
- [ClawHub skill page](https://clawhub.ai/rohitr311/maxun) <br>
- [Publisher profile](https://clawhub.ai/user/rohitr311) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [Plain text and formatted JSON returned from Maxun API calls, with setup guidance in Markdown.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires MAXUN_API_KEY and uses curl, bash, and python3 to call Maxun SDK API endpoints.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
