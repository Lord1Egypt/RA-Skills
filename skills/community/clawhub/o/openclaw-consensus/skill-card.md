## Description:

Run a fixed 2-round cross-model deliberation through the repo-local OpenClaw Consensus runtime.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pstepien-labs](https://clawhub.ai/user/pstepien-labs)

### License/Terms of Use:

MIT-0

## Use Case:

OpenClaw users use this skill to run a bounded two-round deliberation across an explicit shortlist of configured API-backed models, then review a final synthesis that separates consensus, disagreements, uncertainty, and escalation points.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Briefs and model outputs are sent to selected configured model providers and persisted locally in plaintext.

Mitigation: Use only briefs suitable for the chosen providers and local storage, and verify provider retention expectations before running sensitive work.

Risk: The server security summary flags an unsupported gitignore safety claim for run artifacts.

Mitigation: Verify that /runs/ is ignored and review tracked files before publishing or sharing validation artifacts.

Risk: Untrusted --run-root paths could redirect where run artifacts are written.

Mitigation: Use default run directories or reviewed paths, and do not accept --run-root values from untrusted parties.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/pstepien-labs/skills/openclaw-consensus)
- [README](README.md)
- [Runtime Contract](docs/RUNTIME_CONTRACT.md)
- [Prompt Contract](docs/PROMPT_CONTRACT.md)
- [Commands](docs/COMMANDS.md)
- [Validation Evidence](validation/README.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance, files]

**Output Format:** [Markdown final synthesis with supporting Markdown and JSON run artifacts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates local run artifacts for the original brief, run metadata, each model round, and the final synthesis.]

## Skill Version(s):

0.1.2 (source: package.json and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
