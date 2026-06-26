## Description: <br>
Convert an existing Obsidian Vault into an agent-ready ExpertPack that restructures vault content for EK optimization, RAG retrieval, and OpenClaw integration while creating a copy and leaving the source vault unchanged. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[brianhearn](https://clawhub.ai/user/brianhearn) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to convert Obsidian vaults into ExpertPack knowledge packs for RAG retrieval and OpenClaw memory search. It is suited for preparing copied vault content for validation, enhancement, and indexing without modifying the original vault. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Converted output may include the source vault's hidden `.obsidian/` configuration by default. <br>
Mitigation: Run `--dry-run` first, inspect the generated pack, and remove the copied `.obsidian/` folder before using or sharing the pack if it is not needed. <br>
Risk: Adding the converted pack to OpenClaw defaults can make its contents available to future memory searches. <br>
Mitigation: Index only reviewed output paths and remove the pack path from OpenClaw configuration when the content should no longer be searchable. <br>
Risk: Private or sensitive notes from an Obsidian vault may be copied into an agent-readable ExpertPack. <br>
Mitigation: Review the copied markdown and generated metadata before validation, publishing, or persistent indexing. <br>


## Reference(s): <br>
- [Obsidian Vault to ExpertPack Migration Guide](references/migration-guide.md) <br>
- [ExpertPack homepage](https://expertpack.ai) <br>
- [ClawHub skill page](https://clawhub.ai/brianhearn/obsidian-to-expertpack) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with bash and JSON snippets plus a Python conversion script that writes ExpertPack files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces a copied ExpertPack directory containing converted markdown files, generated manifest.yaml, overview.md, glossary.md, per-directory _index.md files, and copied .obsidian configuration when present.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
