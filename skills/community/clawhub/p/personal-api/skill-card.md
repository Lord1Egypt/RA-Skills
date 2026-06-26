## Description: <br>
Turn an Obsidian vault into an AI-readable personal identity layer for setting up ME.md, AGENT.md, agent adapter files, and the optional Knowledge Palace v2 scaffold. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[beiyuii](https://clawhub.ai/user/beiyuii) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to scaffold an Obsidian vault so AI agents can read personal context, collaboration rules, and knowledge-system navigation. It helps install or refresh the identity layer, add thin adapter files for agent runtimes, and optionally create the Knowledge Palace v2 structure. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The setup script writes scaffold files into the Obsidian vault path selected by the user. <br>
Mitigation: Install only into the intended vault and check OBSIDIAN_VAULT_PATH before running setup.sh. <br>
Risk: Full setup creates the 30.knowledge Knowledge Palace v2 structure, which may be more than an identity-only user expects. <br>
Mitigation: Use --minimal when the user wants only ME.md, AGENT.md, and lightweight adapter files. <br>
Risk: Filled-in ME.md and AGENT.md are designed to contain personal identity, preferences, and working context. <br>
Mitigation: Treat completed vault files as private and avoid committing or publishing real personal content. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/beiyuii/personal-api) <br>
- [architecture.md](references/architecture.md) <br>
- [vault-layout.md](references/vault-layout.md) <br>
- [operation-boundaries.md](references/operation-boundaries.md) <br>
- [maintenance.md](references/maintenance.md) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and generated vault template files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates or refreshes local Obsidian vault scaffolding; filled-in identity files should be treated as private user content.] <br>

## Skill Version(s): <br>
2.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
