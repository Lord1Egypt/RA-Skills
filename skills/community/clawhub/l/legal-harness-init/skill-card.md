## Description:

Helps legal professionals safely generate, incrementally merge, and verify persistent AGENTS.md/CLAUDE.md collaboration and legal-safety baselines.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cat-xierluo](https://clawhub.ai/user/cat-xierluo)

### License/Terms of Use:

MIT

## Use Case:

Legal professionals, law-firm teams, in-house legal teams, and compliance users use this skill to initialize or update persistent agent instruction files for AGENTS.md/CLAUDE.md. It focuses on privacy posture, permission boundaries, traceability expectations, safe managed-block updates, and fresh-session behavior checks rather than legal analysis or document drafting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent AGENTS.md/CLAUDE.md files may expose sensitive legal matter details if users place client facts, credentials, or high-sensitivity identifiers in long-lived configuration.

Mitigation: Use the skill's strict, local, or team privacy modes; review the dry-run diff and target paths before writing; keep real client facts and credentials out of persistent configuration, logs, commits, and external services.

Risk: The skill can create or update persistent agent instruction files, so an unintended target path or managed-block update could change future agent behavior.

Mitigation: Run detection first, inspect the proposed targets, use dry-run output before removing the dry-run flag, and rely on the managed-block, backup, and restore workflow for controlled updates.

Risk: Behavior verification is useful evidence of a fresh-session check but should not be treated as a tamper-proof security attestation.

Mitigation: Treat BEHAVIOR_VERIFIED as operator-managed evidence, bind checks to a fresh session and current configuration hash, and avoid escalating CONFIG_WRITTEN into loaded or behavior-verified status without matching evidence.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cat-xierluo/skills/legal-harness-init)
- [Project homepage](https://github.com/cat-xierluo/legal-skills)
- [03 - Harness detection](references/03-harness-detection.md)
- [05 - Writing a good AGENTS.md](references/05-write-an-agents-md.md)
- [06 - Legal traceability contract](references/06-audit-trail-contract.md)
- [18 - Privacy modes and minimum necessary context](references/18-privacy-and-context.md)
- [19 - Fresh-session loading and behavior verification](references/19-activation-verification.md)
- [20 - Three-layer team instruction governance](references/20-team-layering.md)
- [Scripts usage guide](scripts/README.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands, managed AGENTS.md/CLAUDE.md configuration blocks, and JSON status from helper scripts.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports dry-run review before writing, managed-block updates, content validation, backup/restore workflow, and fresh-session verification evidence.]

## Skill Version(s):

0.3.0 (source: frontmatter, CHANGELOG, server release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
