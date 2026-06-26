## Description: <br>
Fetches GitHub repository content with curl so an agent can analyze, review, explore, or understand a repository from current source files. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shiscofield12-beep](https://clawhub.ai/user/shiscofield12-beep) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and technical users use this skill to inspect GitHub repositories by fetching repository listings, README files, and specific source files before forming an analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill contacts GitHub to fetch repository contents, which may expose requested repository names or paths to GitHub. <br>
Mitigation: Use it only when outbound GitHub access is acceptable; avoid private repositories unless authentication and data handling have been reviewed. <br>
Risk: Fetched repository content may be incomplete or rate-limited when using unauthenticated GitHub requests. <br>
Mitigation: Verify important findings against fetched files and retry with the correct branch or approved authentication when needed. <br>
Risk: Fetched code may be unsafe to execute. <br>
Mitigation: Treat fetched repository content as untrusted and review code before running commands from it. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/shiscofield12-beep/github-fetcher) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and repository analysis] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl and network access to GitHub; analysis should be based on fetched repository content.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
