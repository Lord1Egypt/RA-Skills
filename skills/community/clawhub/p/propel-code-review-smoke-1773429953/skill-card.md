## Description: <br>
Run async diff-based code reviews using the Propel Review API, poll for completion, retrieve structured findings, and send comment feedback. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jasonyuezhang](https://clawhub.ai/user/jasonyuezhang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering agents use this skill to submit repository diffs to Propel for asynchronous code review, poll for structured review comments, and report whether each comment was incorporated. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Repository diffs are submitted to Propel for review. <br>
Mitigation: Install and run only when the user trusts Propel with the diffs being reviewed; show the diff or review payload before submission when handling sensitive repositories. <br>
Risk: The skill can persist a Propel API token in a shell profile. <br>
Mitigation: Prefer setting PROPEL_API_KEY only for the active session or through a secret manager, and avoid printing token values in logs or chat. <br>
Risk: The workflow can edit code and post comment feedback without a separate confirmation step. <br>
Mitigation: Require the agent to show proposed code changes and feedback payloads before applying changes or sending feedback. <br>


## Reference(s): <br>
- [Propel homepage](https://www.propelcode.ai/) <br>
- [ClawHub skill page](https://clawhub.ai/jasonyuezhang/propel-code-review-smoke-1773429953) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON API payloads or responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires PROPEL_API_KEY plus curl, git, and jq; review payloads may include repository diffs.] <br>

## Skill Version(s): <br>
0.0.1 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
