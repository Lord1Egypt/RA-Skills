## Description: <br>
Manage Threads accounts, OAuth connect URLs, drafts, and publishing through the local threadsctl CLI. Use when the user wants to post to Threads, create or publish drafts, connect accounts, inspect stats, or work with image, carousel, or spoiler media posts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dladislav201](https://clawhub.ai/user/dladislav201) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to manage Threads account connection, drafts, publishing, stats, and media posting workflows through the local threadsctl CLI. It is useful when an agent should prefer the deployed CLI over raw HTTP calls and should distinguish draft-first from immediate publishing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can publish publicly to Threads or publish approved drafts through threadsctl. <br>
Mitigation: Confirm the target account and post content before publishing, use draft-first workflows unless immediate posting is clearly requested, and use --confirmed only when the user intends direct publication. <br>
Risk: The skill depends on sensitive Threads service credentials. <br>
Mitigation: Protect THREADS_SERVICE_API_KEY, avoid exposing credentials in messages or logs, and install only when the local threadsctl CLI and deployed Threads service are trusted. <br>
Risk: OAuth connect URLs can affect account access. <br>
Mitigation: Generate connect URLs only for the requested account label and have the user complete the OAuth flow deliberately. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dladislav201/openclaw-threadsctl) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and concise result summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include Threads account labels, draft IDs, post IDs, and OAuth connect URLs when useful.] <br>

## Skill Version(s): <br>
1.0.3 (source: server evidence release.version) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
