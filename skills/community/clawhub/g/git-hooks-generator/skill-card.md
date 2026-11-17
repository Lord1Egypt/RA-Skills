## Description:

Generates Git hook scripts that format code, check lint rules, and run tests.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sunshine-del-ux](https://clawhub.ai/user/sunshine-del-ux)

### License/Terms of Use:

MIT

## Use Case:

Developers and engineering teams use this skill to initialize repository-local Git hooks for pre-commit lint and test checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The generated pre-commit hook can overwrite an existing .git/hooks/pre-commit file.

Mitigation: Inspect the generated hook and preserve or merge any existing pre-commit behavior before enabling it.

Risk: The generated hook runs npm run lint and npm test on future commits.

Mitigation: Confirm the repository's npm scripts are expected and safe to run before installing the hook.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sunshine-del-ux/skills/git-hooks-generator)

## Skill Output:

**Output Type(s):** [Shell commands, Code, Configuration]

**Output Format:** [Markdown with inline bash commands and generated Git hook script content]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates a repository-local .git/hooks/pre-commit script that runs npm lint and test commands.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact/_meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
