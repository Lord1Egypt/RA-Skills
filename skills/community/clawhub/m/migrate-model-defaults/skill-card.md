## Description:

Find, classify, and update hardcoded default-like model references in a repo.

This skill is ready for commercial/non-commercial use.

## Publisher:

[patrick-erichsen-2](https://clawhub.ai/user/patrick-erichsen-2)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to audit and migrate repository model defaults while avoiding broad replacement of tests, examples, catalogs, and compatibility references.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Optional workflow validation may run actionlint through Go using an unpinned '@latest' dependency when actionlint is not already installed.

Mitigation: Use a preinstalled or pinned actionlint version in sensitive repositories.

Risk: Repo-editing guidance can affect default model behavior if irrelevant references are selected for update.

Mitigation: Review the presented candidate checklist and approve only intended default-like references before edits.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/patrick-erichsen-2/skills/migrate-model-defaults)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with file references, checklists, inline commands, and code/configuration edits]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Asks for the existing and replacement model strings, presents candidate edits for user selection, and validates workflow changes when applicable.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
