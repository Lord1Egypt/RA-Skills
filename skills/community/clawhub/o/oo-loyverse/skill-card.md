## Description: <br>
Loyverse (loyverse.com). Use this skill for ANY Loyverse request - searching and reading data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to look up Loyverse merchant, store, category, item, customer, and receipt data through an OOMOL-connected account. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a connected Loyverse account and OOMOL oo CLI access, so failed or unnecessary setup steps could expose authentication or billing workflows. <br>
Mitigation: Install only when the user intends to use OOMOL's oo CLI with a connected Loyverse account; run setup, billing, or authentication steps only after a matching command failure or explicit user request. <br>
Risk: The current action list is read-only, but future connector actions may change Loyverse state. <br>
Mitigation: Treat this release as a read-only lookup helper and confirm the exact payload and effect before any future write or destructive action. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/oomol/oo-loyverse) <br>
- [OOMOL publisher profile](https://clawhub.ai/user/oomol) <br>
- [Loyverse homepage](https://loyverse.com/) <br>
- [oo CLI](https://github.com/oomol-lab/oo-cli) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON connector responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses live connector schema inspection before action execution; connector responses include data and meta.executionId.] <br>

## Skill Version(s): <br>
1.0.1 (source: server evidence release.version and frontmatter metadata.version) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
