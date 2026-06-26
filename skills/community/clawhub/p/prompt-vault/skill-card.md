## Description: <br>
Organize, rate, and share prompts with your team through a local command-line prompt library with JSON storage, search, import/export, and static HTML browsing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[TheShadowRose](https://clawhub.ai/user/TheShadowRose) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers, prompt engineers, and teams use this skill to maintain a shared local prompt library, track ratings and usage, exchange prompt vaults, and generate a static browse page for review. It is best suited for prompt curation workflows where users control the local vault file and sharing process. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompt vaults are stored as plaintext local JSON and may contain sensitive prompt content. <br>
Mitigation: Do not store credentials, regulated personal data, or confidential workflows unless the vault location is protected with appropriate filesystem permissions or encryption. <br>
Risk: Exported JSON vaults and generated HTML browse pages can accidentally disclose prompt contents when shared. <br>
Mitigation: Review exported files and generated HTML before sharing them outside the intended team. <br>
Risk: Imported vault files can replace or merge local prompt content. <br>
Mitigation: Import vault files only from trusted sources and review replace or merge behavior before applying changes. <br>
Risk: Concurrent edits can overwrite changes because the tool does not provide file locking or automatic conflict resolution. <br>
Mitigation: Use Git, coordinated edit windows, or another external sync process when multiple people maintain the same vault. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/TheShadowRose/prompt-vault) <br>
- [README.md](artifact/README.md) <br>
- [LIMITATIONS.md](artifact/LIMITATIONS.md) <br>
- [LICENSE.md](artifact/LICENSE.md) <br>
- [config_example.json](artifact/config_example.json) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with Python and shell command examples; bundled scripts produce JSON vault files and static HTML browse pages.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses local files and Python standard-library scripts; no hosted service or AI API integration is provided.] <br>

## Skill Version(s): <br>
1.0.0 (source: SKILL.md frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
