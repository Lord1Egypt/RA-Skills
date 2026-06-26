## Description: <br>
Lint and validate package.json files for common mistakes, missing fields, security issues, and best practices. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[charlie-morrison](https://clawhub.ai/user/charlie-morrison) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and maintainers use this skill to lint package.json files, validate npm package metadata, inspect dependency and script issues, and produce review-ready reports before publishing or changing Node.js projects. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security mode is heuristic script-risk checking, not a full npm vulnerability audit. <br>
Mitigation: Use it as a local package.json review aid and run dedicated dependency vulnerability tooling before release. <br>
Risk: Directory scans read package.json files under the selected project path. <br>
Mitigation: Run the skill against a specific package.json file or intended project directory. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/charlie-morrison/package-json-linter) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, guidance] <br>
**Output Format:** [Text, JSON, or Markdown lint reports with shell command guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Exit code 1 is used when errors are found or when strict mode treats warnings as failures.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
