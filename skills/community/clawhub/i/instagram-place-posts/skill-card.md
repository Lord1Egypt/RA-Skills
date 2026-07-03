## Description: <br>
Scrapes Instagram posts tagged at a specific location or place, returning media items with captions, like/comment counts, media URLs and user info. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[browseract-cli](https://clawhub.ai/user/browseract-cli) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users use this skill to search Instagram locations and collect paginated posts associated with a selected place from a logged-in browser session. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses a logged-in Instagram browser session and internal Instagram APIs to scrape paginated location posts. <br>
Mitigation: Install only when that access pattern is acceptable, and run it only from an account and browser session authorized for the requested data. <br>
Risk: The security guidance flags stealth multi-session throughput guidance as a concern. <br>
Mitigation: Avoid stealth multi-session throughput workflows and keep scraping serial with appropriate review before batch execution. <br>
Risk: Generated bash scripts and local execution notes may affect the user's environment or retain operational details. <br>
Mitigation: Review generated bash before running it, and delete or monitor the local memory file when retained notes are not wanted. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/browseract-cli/instagram-place-posts) <br>
- [Publisher profile](https://clawhub.ai/user/browseract-cli) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell command templates and JSON API result examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires an active logged-in Instagram browser session and returns paginated location post records.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
