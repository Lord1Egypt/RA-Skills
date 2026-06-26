## Description: <br>
Discover hot topics on X, enrich tweets one-by-one, score and summarize signals, generate one tweet draft, and optionally publish on schedule. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Vmining](https://clawhub.ai/user/Vmining) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to monitor public X topics, rank current signals, generate a concise tweet draft, and optionally publish it or schedule recurring posts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can publish public posts to X when write-capable OAuth credentials are provided and --post is used. <br>
Mitigation: Use search or draft mode first, review generated text before posting, and provide write credentials only when publishing is intended. <br>
Risk: The skill can create a recurring scheduled posting workflow. <br>
Mitigation: Enable the cron job only when ongoing automatic public posts are acceptable and document how to remove or disable the schedule. <br>
Risk: The security verdict is suspicious because publishing can occur without a separate approval step. <br>
Mitigation: Review the skill carefully before installing it on any important X account. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Vmining/kiro-x-publisher) <br>
- [X](https://x.com) <br>
- [Cron command example](examples/cron_command.txt) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with shell commands; runtime files include latest.json and latest.txt] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Search mode requires X_BEARER_TOKEN; posting requires X OAuth write credentials.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
