## Description:

Verifies agent-to-agent communication against session type protocols with local formal checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rafapra3008](https://clawhub.ai/user/rafapra3008)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use this skill to parse Lingua Universale protocols, verify message sequences, check declared safety properties, and browse standard protocol templates before or after agent communication.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unpinned package or dependency installation through uvx or pip can retrieve code that differs from the reviewed release.

Mitigation: Install only from a trusted package source, pin the exact reviewed version, and run the MCP server with least privilege.

Risk: Verification results depend on the correctness and completeness of the protocol text and message history supplied to the tools.

Mitigation: Review protocol definitions before use and validate full transcripts when relying on results for workflow decisions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/rafapra3008/skills/lingua-universale)
- [Lingua Universale repository](https://github.com/rafapra3008/cervellaswarm)

## Skill Output:

**Output Type(s):** [text, configuration, guidance]

**Output Format:** [JSON strings returned by MCP tools, plus Markdown setup guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Runs locally for protocol verification and requires Python 3.11 or newer.]

## Skill Version(s):

0.1.0 (source: server release, SKILL.md frontmatter, pyproject.toml)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
