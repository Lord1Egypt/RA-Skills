## Description:

Prepare, safety-review, version, commit, and publish local Codex skills through a GitHub-backed release flow and ClawHub CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jichengkai](https://clawhub.ai/user/jichengkai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and skill maintainers use this skill to prepare local Codex skills for GitHub-backed release, run pre-publish safety checks, and publish or update skills through ClawHub.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The bundled scanner can follow file symlinks outside the selected skill folder and read unintended local files.

Mitigation: Do not run the scanner on untrusted skill directories or archives until symlinks are checked or the scanner is updated to skip symlinks and use bounded reads.

Risk: Publishing workflows can trigger state-changing git, GitHub, or ClawHub actions.

Mitigation: Confirm the target skill path and publish destination before running commands, and require local authentication or secret setup without exposing credentials in chat or source files.

## Reference(s):

- [Publishing Flow](references/publishing.md)
- [Security Review](references/security-review.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces publication guidance, safety-review findings, release notes, and exact manual or automated publish commands.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
