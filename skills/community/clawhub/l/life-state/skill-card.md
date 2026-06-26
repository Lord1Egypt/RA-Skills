## Description: <br>
Daily mood / energy / soreness / sleep capture primitive. Other lifekit skills read this to make state-aware suggestions instead of generic templates. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dsdevq](https://clawhub.ai/user/dsdevq) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and agent builders use this skill to capture daily mood, energy, sleep quality, soreness, and notes in local files so other lifekit skills can adapt their suggestions to current state. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Mood, sleep, soreness, energy, and free-text notes are stored locally in plaintext. <br>
Mitigation: Avoid logging highly sensitive details and restrict access to the local ~/.life/state directory. <br>
Risk: Casual statements such as "I feel..." could be interpreted as state to log. <br>
Mitigation: Have the agent confirm user intent before writing personal state entries. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dsdevq/life-state) <br>
- [Publisher profile](https://clawhub.ai/user/dsdevq) <br>
- [lifekit framework](https://github.com/dsdevq/lifekit) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [YAML on stdout for CLI results, with agent guidance in Markdown.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Stores one plaintext JSON file per day under ~/.life/state when the CLI set command is used.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata, SKILL.md frontmatter, package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
