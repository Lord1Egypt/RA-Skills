## Description:

High-precision memory with 100% recall accuracy for long contexts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mhndayesh](https://clawhub.ai/user/mhndayesh)

### License/Terms of Use:


## Use Case:

Developers and OpenClaw users use this skill to store project text in a local memory service and retrieve prior facts through recall and ingest commands.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Private or sensitive memory may be exposed or retained too broadly.

Mitigation: Use only non-sensitive data unless the service is bound to localhost, authenticated, isolated per user, and governed by clear deletion and retention controls.

Risk: The autonomous integration guidance can weaken normal safety checks by treating recalled content as absolute ground truth.

Mitigation: Do not add the AUTO_INTEGRATION identity-file block as written; treat recalled facts as retrieved evidence that should be checked before use.

Risk: Unpinned dependencies and a local sidecar increase installation and runtime review burden.

Mitigation: Pin and review dependencies before deployment and review the sidecar configuration before running it.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mhndayesh/skills/infinite-memory-v2)
- [INSTALL.md](INSTALL.md)
- [AUTO_INTEGRATION.md](references/AUTO_INTEGRATION.md)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Plain text responses and Markdown setup guidance with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Recall responses are returned as local text; setup requires a running local memory service and local LM Studio endpoint.]

## Skill Version(s):

1.0.0 (source: server release and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
