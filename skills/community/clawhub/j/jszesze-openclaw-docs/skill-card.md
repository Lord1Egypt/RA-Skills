## Description: <br>
OpenClaw Docs helps agents cache the live OpenClaw docs index, search page titles and URLs, fetch raw Markdown pages, build a local full-text docs cache, and track index snapshots over time. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jszesze](https://clawhub.ai/user/jszesze) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and technical support agents use this skill to answer OpenClaw setup, configuration, CLI, channel, automation, architecture, and troubleshooting questions with grounded docs links and current page text. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The helper scripts fetch public web content and write a local docs cache. <br>
Mitigation: Keep fetches to docs.openclaw.ai unless intentionally retrieving another URL, and review shell script execution in environments with strict network or shell controls. <br>
Risk: Cached snippets or documentation pages can become stale. <br>
Mitigation: Refresh or fetch the current OpenClaw documentation before giving operational configuration guidance. <br>


## Reference(s): <br>
- [OpenClaw Docs index](https://docs.openclaw.ai/llms.txt) <br>
- [OpenClaw Telegram docs](https://docs.openclaw.ai/channels/telegram) <br>
- [OpenClaw Docs release page](https://clawhub.ai/jszesze/jszesze-openclaw-docs) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with documentation links, fetched page excerpts, inline shell commands, and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write a local cache of public OpenClaw documentation when its helper scripts are run.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
