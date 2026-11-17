## Description:

Query Chinese labor law on overtime, leave, contracts, and severance rules.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ckchzh](https://clawhub.ai/user/ckchzh)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers can use this skill to obtain Chinese labor-law reference output for worker rights, overtime, leave, contracts, disputes, and severance. The package also documents local command-line logging commands, so users should verify the intended entrypoint before handling sensitive legal or employment information.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The server security summary says the skill is advertised as a Chinese labor-law helper while the main documented command flow is a generic plaintext local logging tool.

Mitigation: Review the intended entrypoint before installation or use, align documentation with the labor-law script behavior, and avoid relying on the package until that mismatch is resolved.

Risk: The server security guidance warns that contracts, employee identifiers, wage records, dispute facts, or privileged legal notes could be stored locally in plaintext under the invoking user's permissions.

Mitigation: Do not enter sensitive legal or employment data unless plaintext local storage is acceptable; use a controlled LABOR_LAW_DIR and inspect or remove local data.log and history.log files after use.

Risk: The artifact presents legal reference information that may not account for local rules or case-specific facts.

Mitigation: Treat outputs as general legal knowledge only and consult a qualified labor-law professional for specific disputes or decisions.

## Reference(s):

- [Labor Law ClawHub Page](https://clawhub.ai/ckchzh/skills/labor-law)
- [BytesAgain Homepage](https://bytesagain.com)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown and terminal text from Bash scripts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Documented utility commands may write plaintext data.log and history.log files under the invoking user's local data directory.]

## Skill Version(s):

2.0.1 (source: server release metadata; artifact frontmatter reports 2.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
