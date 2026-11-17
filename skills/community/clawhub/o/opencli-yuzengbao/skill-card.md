## Description:

OpenCLI turns websites, Electron apps, and local tools into command-line interfaces with built-in commands for services such as Bilibili, Twitter/X, Reddit, Xiaohongshu, GitHub, Hacker News, arXiv, Stack Overflow, and Product Hunt.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yuzengbaao](https://clawhub.ai/user/yuzengbaao)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to install and operate OpenCLI commands that expose websites, authenticated browser sessions, public APIs, Electron apps, and local tools through a CLI interface. It also guides developers through creating new OpenCLI adapters from discovered web APIs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks users to install OpenCLI from npm and a Browser Bridge extension from a release package.

Mitigation: Verify the npm package, extension source, and publisher before installing or running commands.

Risk: Some commands reuse logged-in Chrome sessions and may access authenticated website data.

Mitigation: Use a dedicated Chrome profile with only the accounts needed for the task and avoid sensitive accounts.

Risk: Some OpenCLI commands may auto-install tools or inspect authenticated web requests.

Mitigation: Review command behavior before execution and run it in a constrained environment where practical.

## Reference(s):

- [OpenCLI ClawHub skill page](https://clawhub.ai/yuzengbaao/skills/opencli-yuzengbao)
- [ClawHub publisher profile: yuzengbaao](https://clawhub.ai/user/yuzengbaao)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include commands that interact with public APIs, local CLIs, or logged-in Chrome browser sessions depending on the selected OpenCLI command.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
