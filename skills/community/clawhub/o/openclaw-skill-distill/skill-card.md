## Description: <br>
Skill Distill helps agents turn a local project into a clean, publishable ClawHub skill by scanning for local traces, scaffolding standard files, and validating before publish. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yuchangxu1989-openclaw](https://clawhub.ai/user/yuchangxu1989-openclaw) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent authors use Skill Distill to extract an existing project into a reusable ClawHub skill, check for secrets or hardcoded local paths, scaffold standard skill files, and validate the package before publishing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Project-derived files may be uploaded to ClawHub before secrets, proprietary code, private paths, customer data, or identifying metadata are reviewed. <br>
Mitigation: Review the generated skill directory before publishing, run the provided scan and validation steps, and publish only after confirming exactly which files are included. <br>
Risk: Sensitive credentials or local configuration may remain in material copied from an existing project. <br>
Mitigation: Remove real secrets, private configuration, and local identifiers; replace required credentials with documented placeholders or environment-variable guidance. <br>


## Reference(s): <br>
- [Skill Distill checklist](references/checklist.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with bash commands and generated skill files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create, scan, or validate a skill directory when the included scripts are run.] <br>

## Skill Version(s): <br>
0.2.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
