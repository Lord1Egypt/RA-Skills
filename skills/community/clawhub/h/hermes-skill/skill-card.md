## Description: <br>
HermesSkill gives AI agents self-learning, automatic skill creation, tiered memory management, nudge reminders, scheduled self-checks, and upstream Hermes Agent tracking. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[devrobbin](https://clawhub.ai/user/devrobbin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to add persistent memory, nudge-based reflection, generated reusable skills, skill evaluation, and upstream Hermes Agent change tracking to a coding or automation agent. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent agent memory can retain sensitive personal data, credentials, private prompts, or project details. <br>
Mitigation: Keep secrets and sensitive personal data out of memory, and periodically inspect and prune the local self-improvement files. <br>
Risk: Generated or improved skills can change future agent behavior without enough human review. <br>
Mitigation: Require manual approval and scanning before generated or modified skills become active. <br>
Risk: Scheduled checks and upstream tracking can fetch remote data and write local state files. <br>
Mitigation: Enable scheduled checks only intentionally, review network access, and inspect tracker state and changelog outputs. <br>
Risk: The artifact encourages GitHub publishing as part of its self-evolution workflow. <br>
Mitigation: Require explicit user approval before any git commit, push, or publication step. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/devrobbin/hermes-skill) <br>
- [Project homepage](https://github.com/devrobbin/hermes-skill) <br>
- [Hermes Agent upstream repository](https://github.com/nousresearch/hermes-agent) <br>
- [Hermes Agent documentation](https://hermes-agent.nousresearch.com/docs/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown, JSON, plain text, generated skill files, and shell command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands may write local memory, nudge, evaluation, generated skill, and upstream-tracker files under the user's home directory.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence; artifact frontmatter states 1.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
