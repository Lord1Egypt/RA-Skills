## Description:

Mistake-proofing technique manager. Use when json poka yoke tasks, csv poka yoke tasks, checking poka yoke status.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ckchzh](https://clawhub.ai/user/ckchzh)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to manage local poka-yoke records, including adding, listing, searching, removing, exporting, and configuring entries for mistake-proofing workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The ClawHub security scan reports a suspicious verdict because an unsafe config command can be abused to run shell commands.

Mitigation: Review before installing, use only trusted local input, and avoid passing untrusted text to config until the command-injection issue is fixed.

Risk: The scan summary and guidance note weak safeguards around JSON/CSV escaping, remove operations, and export overwrite behavior.

Mitigation: Do not use this release for sensitive records; review exported data, confirm destructive removals manually, and avoid overwriting important files until these behaviors are fixed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ckchzh/skills/poka-yoke)
- [BytesAgain homepage](https://bytesagain.com)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and plain-text command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update local JSONL data, configuration text, and export files under the configured POKA_YOKE_DIR or current working directory.]

## Skill Version(s):

1.0.0 (source: server evidence release.version and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
