## Description:

Daily mood / energy / soreness / sleep capture primitive. Other lifekit skills read this to make state-aware suggestions instead of generic templates.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dsdevq](https://clawhub.ai/user/dsdevq)

### License/Terms of Use:

MIT

## Use Case:

External users and agent builders use this skill to capture daily mood, energy, soreness, sleep quality, and notes so related personal-AI skills can adapt suggestions to current state.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores mood, sleep, soreness, and personal notes as plaintext JSON under the user's home directory by default.

Mitigation: Use it only on trusted machines and storage locations; set LIFE_STATE_DIR to a private or container-local path when isolation is needed.

Risk: Free-form personal notes are passed to a Bash-invoked CLI, which can create command-execution risk if agents concatenate raw user text into shell commands.

Mitigation: Invoke life-state with structured arguments and safe argument passing rather than building shell strings from untrusted text.

Risk: Broad conversational triggers can cause personal state to be captured more often than intended.

Mitigation: Prefer explicit check-in commands and confirm tersely what was recorded.

## Reference(s):

- [Life State ClawHub release page](https://clawhub.ai/dsdevq/skills/life-state)
- [Publisher profile](https://clawhub.ai/user/dsdevq)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration, Guidance]

**Output Format:** [Plain text guidance with shell command examples and YAML-producing CLI calls]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes and reads plaintext daily JSON state through the life-state CLI.]

## Skill Version(s):

0.2.0 (source: server release metadata and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
