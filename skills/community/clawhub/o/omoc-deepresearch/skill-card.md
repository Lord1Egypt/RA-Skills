## Description:

Deep research workflow for /deepresearch with sources, claims, synthesis, and resumable state.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jkobject](https://clawhub.ai/user/jkobject)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, researchers, and analysts use this skill to run source-grounded investigations that need durable state, evidence tracking, and resumable synthesis across agent turns.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A path-like or untrusted slug could direct the helper script to read or write a ledger outside the intended .deepresearch folder.

Mitigation: Use trusted slugs only and prefer a fixed version that validates slugs before reading or writing ledger files.

Risk: The skill creates persistent .deepresearch state in the workspace.

Mitigation: Install and run it only in workspaces where this local research ledger state is acceptable.

Risk: Non-/deepresearch prompts could activate the workflow more broadly than intended.

Mitigation: Confirm activation criteria during review and prefer versions that require explicit activation for broader research requests.

## Reference(s):

- [Deep Research on ClawHub](https://clawhub.ai/jkobject/skills/omoc-deepresearch)
- [jkobject publisher profile](https://clawhub.ai/user/jkobject)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, files, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON ledger files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates or updates .deepresearch ledger state when its helper commands are run.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
