## Description: <br>
Validate and pretty-print JSON files from the terminal. Use when linting config files, formatting API payloads, checking syntax before deployment. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bytesagain3](https://clawhub.ai/user/bytesagain3) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use Jsonlint to validate, format, minify, compare, inspect, and extract values from local JSON files in terminal workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Commands that format, minify, diff, list keys, or extract values can print sensitive JSON contents into the terminal or agent session. <br>
Mitigation: Avoid running these commands on JSON files that contain secrets unless the user is comfortable exposing those values in terminal output. <br>
Risk: The tool depends on a local python3 runtime. <br>
Mitigation: Confirm python3 is available before relying on the skill in an environment. <br>


## Reference(s): <br>
- [Jsonlint on ClawHub](https://clawhub.ai/bytesagain3/jsonlint) <br>
- [BytesAgain](https://bytesagain.com) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Text, JSON] <br>
**Output Format:** [Terminal text and JSON emitted by local shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reads user-specified local JSON files and prints validation, formatting, comparison, key listing, or extraction results.] <br>

## Skill Version(s): <br>
3.0.0 (source: release evidence and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
