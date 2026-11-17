## Description:

LYGO Forkling is a test champion skill that builds a local fork under CHAMPION_LYRA, runs claim-gated task loops, snapshots local generations, and emits dry-run Star Chart proposal JSON without live ingest or git push.

This skill is ready for commercial/non-commercial use.

## Publisher:

[deepseekoracle](https://clawhub.ai/user/deepseekoracle)

### License/Terms of Use:

MIT No Attribution (MIT-0)

## Use Case:

Developers and agent builders use this skill to run a local self-building test agent loop that creates fork state, verifies falsifiable claims, advances local generations, and prints proposal JSON for human review. It is not intended to replace Lightfather, publish champions, push to git, or write to a live Star Chart.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Running the documented self-check can erase an existing local state/ directory.

Mitigation: Back up existing state before running scripts/self_check.py, or run the self-check only in a disposable or newly installed skill directory.

Risk: The documented install command uses a mutable external installer.

Mitigation: Prefer a pinned installer version or verify installer provenance before using the npx command.

Risk: Generated proposal JSON could be mistaken for a live Star Chart write.

Mitigation: Treat propose output as pending dry-run JSON and require human review plus a separate gated ingest step before any live publication.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/deepseekoracle/skills/lygo-forkling)
- [ClawHub release listing](https://clawhub.ai/deepseekoracle/lygo-forkling)
- [Project homepage](https://github.com/DeepSeekOracle/lygo-protocol-stack/tree/main/docs/skills/lygo-forkling)
- [Security notes](references/SECURITY.md)
- [SkillSpector audit notes](references/SKILLSPECTOR_AUDIT.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands create local state files only when consent flags are used; the propose command prints dry-run JSON.]

## Skill Version(s):

1.0.0 (source: frontmatter, claw.json, release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
