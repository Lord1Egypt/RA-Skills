## Description: <br>
Use this skill when an installed `intervals` CLI should be used to query Intervals.icu, inspect activities, create scheduled workout events, create workout library items, or write wellness data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jonaswide](https://clawhub.ai/user/jonaswide) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, coaches, and athletes use this skill to have an agent operate the installed `intervals` CLI for Intervals.icu reads and user-directed writes. It helps choose between activity queries, scheduled events, reusable workouts, and wellness data updates. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can access an Intervals.icu account through `INTERVALS_API_KEY` or `INTERVALS_ACCESS_TOKEN`. <br>
Mitigation: Confirm `intervals auth status` before use and provide credentials only when account access is intended. <br>
Risk: Create, upsert, and wellness commands can change fitness account data. <br>
Mitigation: Review generated dates and JSON payloads before mutation commands, and run read or verification commands after writes. <br>
Risk: The skill depends on installing and executing the third-party `intervals` CLI. <br>
Mitigation: Install only from trusted release sources and verify the installed binary before using the skill. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jonaswide/intervals-icu-cli) <br>
- [Publisher profile](https://clawhub.ai/user/jonaswide) <br>
- [intervals CLI homepage](https://github.com/jonaswide/intervals-cli) <br>
- [Query Guidance](references/queries.md) <br>
- [Write Patterns](references/writes.md) <br>
- [macOS arm64 installer](https://github.com/jonaswide/intervals-cli/releases/latest/download/intervals_darwin_arm64.tar.gz) <br>
- [macOS amd64 installer](https://github.com/jonaswide/intervals-cli/releases/latest/download/intervals_darwin_amd64.tar.gz) <br>
- [Linux arm64 installer](https://github.com/jonaswide/intervals-cli/releases/latest/download/intervals_linux_arm64.tar.gz) <br>
- [Linux amd64 installer](https://github.com/jonaswide/intervals-cli/releases/latest/download/intervals_linux_amd64.tar.gz) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, JSON] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON payload examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses JSON-first command patterns and recommends read or verification commands around mutations.] <br>

## Skill Version(s): <br>
1.0.1 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
