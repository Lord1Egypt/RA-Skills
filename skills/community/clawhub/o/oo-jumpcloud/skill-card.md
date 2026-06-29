## Description: <br>
Operate JumpCloud through an OOMOL-connected account to search and read systems and system users. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, administrators, and support agents use this skill to inspect JumpCloud system and system-user records through an OOMOL-connected account without handling raw credentials. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can read JumpCloud systems and system users through the user's OOMOL-connected account. <br>
Mitigation: Install only when this read access is intended, and review the OOMOL connection scopes before use. <br>
Risk: Future releases could add write or destructive JumpCloud actions beyond the current read-only behavior. <br>
Mitigation: Review future action lists, security summaries, and connection scopes before approving an upgrade. <br>


## Reference(s): <br>
- [JumpCloud homepage](https://jumpcloud.com/) <br>
- [OOMOL oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [ClawHub skill page](https://clawhub.ai/oomol/skills/oo-jumpcloud) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline bash and JSON snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses live connector schemas before constructing action payloads; read-only JumpCloud actions return JSON data through the OOMOL CLI.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
