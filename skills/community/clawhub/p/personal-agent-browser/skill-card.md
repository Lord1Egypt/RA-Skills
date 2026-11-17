## Description:

Personal Agent Browser lets an AI assistant call a locally installed agent-browser CLI to fetch a web page and return its title, Markdown content, and a short summary as JSON.

This skill is ready for commercial/non-commercial use.

## Publisher:

[awublack](https://clawhub.ai/user/awublack)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to let an assistant inspect a user-supplied web page through a local CLI and summarize the extracted page content.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: URL handling can execute shell commands when user-controlled input is passed to the browser script.

Mitigation: Review before installing; replace shell execution with argument-safe process spawning and restrict URL schemes and private/internal destinations before using sensitive URLs.

Risk: Privacy and dependency claims may understate that browsing is network activity visible to destination sites and depends on an external CLI.

Mitigation: Treat browsing as network activity, avoid sensitive URLs until controls are added, and pin or locally control the agent-browser dependency.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/awublack/skills/personal-agent-browser)

## Skill Output:

**Output Type(s):** [text, markdown, JSON]

**Output Format:** [Structured JSON containing success, URL, title, extracted Markdown content, and summary fields.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js and a locally installed agent-browser CLI; browsing requests are visible to destination sites.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
