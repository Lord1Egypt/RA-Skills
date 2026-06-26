## Description: <br>
Controls browser automation tasks through a local page-agent service running on localhost:4222, including opening pages, performing page actions, and extracting information. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ucasYToo](https://clawhub.ai/user/ucasYToo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and automation users use this skill to have an agent check a local browser-control service, start it if needed, and submit browser tasks through HTTP endpoints. It is intended for workflows that require opening web pages, interacting with pages, or extracting page information from a local browser session. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can direct an agent to control a user's real browser session, including authenticated pages or sensitive account workflows. <br>
Mitigation: Use an isolated browser profile or test account and require explicit confirmation before logins, payments, account changes, uploads, downloads, form submissions, or reading authenticated pages. <br>
Risk: The workflow depends on a globally installed external CLI for browser control. <br>
Mitigation: Install only when browser control is intentional and verify the release before installing or updating the CLI globally. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ucasYToo/page-agent-claw) <br>
- [Publisher profile](https://clawhub.ai/user/ucasYToo) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, API calls, Guidance] <br>
**Output Format:** [Markdown with inline bash and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses local HTTP endpoints on localhost:4222 and requires node, npm, curl, page-agent-claw, and the page-agent Chrome extension.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
