## Description: <br>
Best practices for using the Oracle CLI to bundle prompts and selected files for model review across browser and API workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[utromaya-code](https://clawhub.ai/user/utromaya-code) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to prepare high-signal Oracle CLI prompts, choose browser or API execution paths, attach focused file sets, and manage long-running sessions for repo-aware AI review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Selected files or prompts may expose secrets, tokens, or unrelated private source content to an AI provider or browser account. <br>
Mitigation: Use dry-run and files-report before live runs, keep --file selections narrow, and exclude .env files, key files, auth tokens, and other sensitive paths. <br>
Risk: Prompts, selected files, and session artifacts may persist locally or in provider and browser history. <br>
Mitigation: Treat Oracle session storage and provider history as persistent records; review or clean ~/.oracle/sessions and relevant browser or provider history according to local policy. <br>
Risk: Model output is advisory and may be incorrect or incomplete for the target repository. <br>
Mitigation: Verify recommendations against the source code, run appropriate tests, and review changes before applying them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/utromaya-code/prompt-bundler-oracle) <br>
- [Oracle homepage](https://askoracle.dev) <br>
- [Publisher profile](https://clawhub.ai/user/utromaya-code) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown with inline shell commands and workflow guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guidance covers file selection, dry-run previews, browser or API engine choice, session reattachment, and secret-exclusion practices.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
