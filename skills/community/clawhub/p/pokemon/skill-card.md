## Description:

CLI for AI agents to lookup Pokemon info for their humans. Uses PokeAPI. No auth required.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jeffaf](https://clawhub.ai/user/jeffaf)

### License/Terms of Use:

MIT

## Use Case:

External users and agents use this skill to look up Pokemon names, stats, type matchups, and abilities through PokeAPI-backed command examples.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installation instructions fetch executable code from a mutable external repository that was not fully reviewed in the package evidence.

Mitigation: Install only from a trusted source, pin the repository to a reviewed commit, and verify a checksum or signature before making scripts executable.

Risk: The skill depends on local shell execution and required binaries.

Mitigation: Run it in a controlled agent environment with bash, curl, and jq installed, and review commands before deployment.

## Reference(s):

- [PokeAPI](https://pokeapi.co)
- [PokeAPI v2 Documentation](https://pokeapi.co/docs/v2)
- [ClawHub skill page](https://clawhub.ai/jeffaf/skills/pokemon)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Plain text and Markdown with inline shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [No authentication required; command usage requires bash, curl, and jq.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
