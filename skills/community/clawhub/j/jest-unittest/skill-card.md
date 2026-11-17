## Description:

Routes Jest unit-testing requests to sub-skills that check component coverage, add tests toward full coverage, and diagnose or repair failing tests.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vuact](https://clawhub.ai/user/vuact)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill in Jest-based front-end projects to inspect component test coverage, generate or update tests, and diagnose test failures or console warnings.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Crafted component names may lead scripts to run unintended shell commands or delete unintended coverage directories.

Mitigation: Use only in trusted repositories with trusted component names; validate component names and enforce path containment before normal use.

Risk: The skill invokes local Jest through generated command strings, including npx-based checks.

Mitigation: Use a locked local Jest installation, review generated configuration before execution, and disable implicit npx installs.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/vuact/skills/jest-unittest)
- [Bundled README](artifact/README.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration]

**Output Format:** [Markdown and JSON summaries with inline shell commands and code edits]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update Jest test files and project-local configuration under the skill's .temp directory.]

## Skill Version(s):

1.0.3 (source: server release evidence and artifact/_meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
