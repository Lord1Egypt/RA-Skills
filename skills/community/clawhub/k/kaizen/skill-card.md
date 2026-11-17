## Description:

Kaizen continuous improvement reference for event planning, PDCA cycles, gemba walks, A3 problem solving, and documenting process changes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xueyetianya](https://clawhub.ai/user/xueyetianya)

### License/Terms of Use:

MIT-0

## Use Case:

External users, employees, and process-improvement practitioners use this skill for Kaizen event preparation, PDCA coaching, gemba walk prompts, A3 report structure, and daily continuous improvement guidance. Reviewers should account for the included local tracker behavior before deployment.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The script creates persistent local files under ~/.kaizen or KAIZEN_DIR.

Mitigation: Run only in an approved local data directory and review file writes before installation.

Risk: The script can delete and export stored entries.

Mitigation: Back up important local tracker data and restrict use of remove and export commands to trusted operators.

Risk: Security evidence reports unsafe shell handling around configuration.

Mitigation: Review configuration keys and values before use, and avoid passing untrusted input to configuration commands.

## Reference(s):

- [Kaizen ClawHub skill page](https://clawhub.ai/xueyetianya/skills/kaizen)
- [BytesAgain homepage](https://bytesagain.com)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown-oriented guidance with shell command examples and local tracker output.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create, list, search, delete, export, and configure local entries under the configured Kaizen data directory.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
