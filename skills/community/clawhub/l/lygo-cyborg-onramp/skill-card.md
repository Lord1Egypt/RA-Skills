## Description:

LYGO Cyborg Onramp is a public ClawHub onramp that prints local install guidance, maps related LYGO public skills, and points users to the separate SkillHub FULL cyborg kernel package.

This skill is ready for commercial/non-commercial use.

## Publisher:

[deepseekoracle](https://clawhub.ai/user/deepseekoracle)

### License/Terms of Use:

MIT No Attribution (MIT-0)

## Use Case:

Developers and agent operators use this skill to discover the public LYGO onramp, inspect local directions, and find the manual path to the separate FULL cyborg kernel package. It does not download, install, or execute that external package.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may assume the linked FULL ZIP or suggested plugins are safe because this onramp received a clean scan.

Mitigation: Inspect and scan each linked package separately before downloading, installing, or running it.

Risk: Users may mistake this public onramp for the full autonomous kernel.

Mitigation: Treat this release as a directory-style helper only; verify any separate FULL package locally before using it.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/deepseekoracle/skills/lygo-cyborg-onramp)
- [Publisher Profile](https://clawhub.ai/user/deepseekoracle)
- [Security Notes](references/SECURITY.md)
- [Quickstart](examples/quickstart.md)
- [Metadata Homepage](https://github.com/DeepSeekOracle/lygo-protocol-stack/tree/main/docs/skills/lygo-cyborg-onramp)
- [SkillHub FULL Pointer](https://chatagent.ca/lygoskillhub.html#full-lygo)
- [LYGO Guides](https://chatagent.ca/guides/)
- [Continuum Portal](https://chatagent.ca/lygo-continuum.html)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Guidance]

**Output Format:** [Markdown documentation and script output containing plain text, JSON maps, URLs, and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Local-only guidance; the skill does not perform network access, subprocess execution, publishing, or filesystem writes.]

## Skill Version(s):

1.0.0 (source: frontmatter, claw.json, release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
